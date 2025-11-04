import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from catalog.models import Product, Category

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='accounts:login')
def create_order(request):
    cart = Cart(request)
    categories = Category.objects.all()

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid() and cart.items:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    **form.cleaned_data
                )

                for item in cart.items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        qty=item.qty
                    )


            if form.cleaned_data["payment_method"] == "cod":
                with transaction.atomic():
                    for it in order.items.select_related("product"):
                        p = Product.objects.select_for_update().get(pk=it.product_id)
                        if p.stock < it.qty:
                            messages.error(request, f"«{p.title}» осталось {p.stock} шт.")
                            return redirect("cart:detail")
                        p.stock = F("stock") - it.qty
                        p.save(update_fields=["stock"])
                request.session["cart"] = {}
                messages.success(request, f"Заказ №{order.id} создан! Оплата при получении.")
                return redirect("accounts:profile")

            else:
                try:
                    line_items = []
                    for it in order.items.select_related("product"):
                        unit_amount = int(it.price * 100)
                        line_items.append({
                            "price_data": {
                                "currency": "usd",
                                "product_data": {"name": it.product.title},
                                "unit_amount": unit_amount,
                            },
                            "quantity": it.qty,
                        })

                    session = stripe.checkout.Session.create(
                        mode="payment",
                        line_items=line_items,
                        success_url=f"{settings.SITE_DOMAIN}/stripe/success/?order_id={order.id}&session_id={{CHECKOUT_SESSION_ID}}",
                        cancel_url=f"{settings.SITE_DOMAIN}/stripe/cancel/?order_id={order.id}",
                        client_reference_id=str(order.id),
                        metadata={"order_id": str(order.id)},
                    )
                    return redirect(session.url, code=303)

                except Exception as e:
                    messages.error(request, f"Ошибка оплаты: {e}")
                    return redirect("cart:detail")

    else:
        form = OrderCreateForm(initial={"delivery_method": "delivery", "payment_method": "card"})

    return render(request, "orders/create_order.html", {"form": form, "cart": cart, "categories": categories})


def stripe_success(request):
    order_id = request.GET.get("order_id")
    session_id = request.GET.get("session_id")

    if not order_id or not session_id:
        messages.warning(request, "Не удалось подтвердить оплату.")
        return redirect("accounts:profile")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        messages.warning(request, f"Не удалось получить статус оплаты: {e}")
        return redirect("accounts:profile")

    if session.payment_status == "paid":
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(pk=int(order_id))
                if not order.paid:
                    for it in order.items.select_related("product"):
                        p = Product.objects.select_for_update().get(pk=it.product_id)
                        if p.stock < it.qty:
                            messages.error(request, f"Недостаточно товара «{p.title}».")
                            return redirect("cart:detail")
                        p.stock = F("stock") - it.qty
                        p.save(update_fields=["stock"])
                    order.paid = True
                    order.save(update_fields=["paid"])
        except Order.DoesNotExist:
            pass

        request.session["cart"] = {}
        messages.success(request, "Оплата прошла успешно. Спасибо за заказ!")
    else:
        messages.warning(request, "Оплата не подтверждена.")

    return redirect("accounts:profile")


def stripe_cancel(request):
    messages.warning(request, "Оплата отменена. Вы можете выбрать другой способ оплаты или попробовать снова.")
    return redirect("cart:detail")


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature")

    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        order_id = (sess.get("metadata") or {}).get("order_id") or sess.get("client_reference_id")
        if order_id:
            with transaction.atomic():
                try:
                    order = Order.objects.select_for_update().get(pk=int(order_id))
                except Order.DoesNotExist:
                    return HttpResponse(status=200)
                if not order.paid:
                    for it in order.items.select_related("product"):
                        p = Product.objects.select_for_update().get(pk=it.product_id)
                        if p.stock < it.qty:
                            return HttpResponse(status=200)
                        p.stock = F("stock") - it.qty
                        p.save(update_fields=["stock"])
                    order.paid = True
                    order.save(update_fields=["paid"])

    return HttpResponse(status=200)
