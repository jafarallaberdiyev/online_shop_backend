from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from orders.models import Order
from .forms import RegisterForm, ProfileForm, AvatarForm
from .models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next') or 'accounts:profile')
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно.")
        return redirect('accounts:profile')
    return render(request, 'users/registration.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('catalog:index')

@login_required
def profile_view(request):
    Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        aform = AvatarForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and aform.is_valid():
            form.save()
            aform.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
        aform = AvatarForm(instance=request.user.profile)

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related(Prefetch("items__product"))
        .order_by("-created_at")
    )

    return render(
        request, "users/profile.html",
        {"form": form, "aform": aform, "orders": orders}
    )
