# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import AuditLog


def _get_ip(request):
    """Extrae la IP del cliente respetando cabeceras de proxy."""
    if request is None:
        return None
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def on_login_ok(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        email_usado=user.email,
        evento=AuditLog.Evento.LOGIN_OK,
        ip=_get_ip(request),
    )


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    if user is None:
        return
    AuditLog.objects.create(
        user=user,
        email_usado=user.email,
        evento=AuditLog.Evento.LOGOUT,
        ip=_get_ip(request),
    )


@receiver(user_login_failed)
def on_login_fail(sender, credentials, request, **kwargs):
    email = credentials.get('username', '')
    AuditLog.objects.create(
        user=None,
        email_usado=email,
        evento=AuditLog.Evento.LOGIN_FAIL,
        ip=_get_ip(request),
    )
