# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Cambio de contraseña (requiere autenticación)
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/password_change.html',
            success_url='/account/password-change/done/',
        ),
        name='password_change',
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='account/password_change_done.html',
        ),
        name='password_change_done',
    ),
    # Recuperación de contraseña (sin autenticación)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password_reset.html',
            email_template_name='account/email/password_reset_email.txt',
            subject_template_name='account/email/password_reset_subject.txt',
            success_url='/account/password-reset/done/',
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password_reset_confirm.html',
            success_url='/account/reset/done/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
