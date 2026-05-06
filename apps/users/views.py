# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('users:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next', 'users:dashboard'))
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')
    return redirect('users:dashboard')


@login_required
def dashboard_view(request):
    return render(request, 'account/dashboard.html', {'user': request.user})
