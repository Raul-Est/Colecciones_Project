# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.conf import settings
from django.db import models
from django.utils import timezone


class AuditLog(models.Model):

    class Evento(models.TextChoices):
        LOGIN_OK = 'login_ok', 'Login correcto'
        LOGIN_FAIL = 'login_fail', 'Login fallido'
        LOGOUT = 'logout', 'Logout'
        PASSWORD_CHANGE = 'password_change', 'Cambio de contraseña'
        PASSWORD_RESET = 'password_reset', 'Recuperación de contraseña'

    # Usuario autenticado; nulo en logins fallidos con email desconocido
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='usuario',
    )

    # Email introducido en el formulario (útil en LOGIN_FAIL sin user)
    email_usado = models.CharField(
        max_length=254,
        blank=True,
        verbose_name='email usado',
    )

    evento = models.CharField(
        max_length=20,
        choices=Evento.choices,
        verbose_name='evento',
    )

    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='dirección IP',
    )

    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name='fecha y hora',
    )

    class Meta:
        verbose_name = 'registro de auditoría'
        verbose_name_plural = 'registros de auditoría'
        ordering = ['-timestamp']

    def __str__(self):
        quien = self.email_usado or (self.user.email if self.user else '?')
        return f'{self.get_evento_display()} — {quien} — {self.timestamp:%Y-%m-%d %H:%M}'
