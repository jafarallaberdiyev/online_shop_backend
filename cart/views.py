from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from .cart import Cart

def _redirect_back(request, fallback='catalog:catalog'):
    referer = request.META.get('HTTP_REFERER')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()}):
        return redirect(referer)
    return redirect(reverse(fallback))

def detail(request):
    cart = Cart(request)
    return render(request, 'carts/cart.html', {'cart': cart})

@require_POST
def add(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get('qty', 1))
    cart.add(product_id, qty=qty, update=False)
    return _redirect_back(request, fallback='catalog:catalog')

@require_POST
def update(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get('qty', 1))
    cart.add(product_id, qty=qty, update=True)
    return _redirect_back(request, fallback='cart:detail')

@require_POST
def remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return _redirect_back(request, fallback='cart:detail')
    # return redirect('cart:detail')
