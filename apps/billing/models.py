# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.conf import settings
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    """
    Oferta comercial y funcional aplicable a un usuario.
    Los límites numéricos con null=True significan ilimitado.
    """

    class Tier(models.TextChoices):
        FREE = 'free', 'Free'
        PREMIUM = 'premium', 'Premium'

    code = models.CharField(max_length=50, unique=True, verbose_name='código')
    name = models.CharField(max_length=100, verbose_name='nombre')
    tier = models.CharField(
        max_length=20,
        choices=Tier.choices,
        verbose_name='nivel',
    )
    is_active = models.BooleanField(default=True, verbose_name='activo')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='orden')

    # Límites
    max_collections = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='máx. colecciones'
    )
    max_items_total = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='máx. elementos totales'
    )
    max_storage_bytes = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name='almacenamiento máx. (bytes)'
    )

    # Funcionalidades
    can_upload_custom_images = models.BooleanField(
        default=True, verbose_name='puede subir imágenes propias'
    )
    can_use_public_collections = models.BooleanField(
        default=False, verbose_name='puede usar colecciones públicas'
    )
    can_use_groups = models.BooleanField(
        default=False,
        verbose_name='puede crear grupos',
        help_text=(
            'False en free. True en premium. '
            'Si el usuario baja a free, sus grupos existentes se conservan '
            'pero no puede crear nuevos.'
        ),
    )
    can_use_advanced_features = models.BooleanField(
        default=False, verbose_name='puede usar funciones avanzadas'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='actualizado')

    class Meta:
        verbose_name = 'plan'
        verbose_name_plural = 'planes'
        ordering = ['sort_order', 'code']

    def __str__(self):
        return f'{self.name} ({self.code})'


class Subscription(models.Model):
    """
    Relación temporal entre un usuario y un plan.
    Un usuario free no tiene fila aquí; su estado se infiere por ausencia
    de suscripción activa premium.
    """

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Activa'
        SUSPENDED = 'suspended', 'Suspendida'
        CANCELED = 'canceled', 'Cancelada'
        EXPIRED = 'expired', 'Vencida'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='usuario',
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='plan',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name='estado',
    )

    started_at = models.DateTimeField(default=timezone.now, verbose_name='inicio')
    current_period_start = models.DateTimeField(
        null=True, blank=True, verbose_name='inicio periodo actual'
    )
    current_period_end = models.DateTimeField(
        null=True, blank=True, verbose_name='fin periodo actual'
    )
    grace_until = models.DateTimeField(
        null=True, blank=True, verbose_name='gracia hasta'
    )
    canceled_at = models.DateTimeField(
        null=True, blank=True, verbose_name='cancelada en'
    )
    suspended_at = models.DateTimeField(
        null=True, blank=True, verbose_name='suspendida en'
    )
    ended_at = models.DateTimeField(
        null=True, blank=True, verbose_name='finalizada en'
    )
    auto_renew = models.BooleanField(default=True, verbose_name='renovación automática')

    # Datos de pasarela externa (para futuro)
    provider = models.CharField(max_length=50, blank=True, verbose_name='proveedor')
    provider_customer_id = models.CharField(
        max_length=200, blank=True, verbose_name='ID cliente externo'
    )
    provider_subscription_id = models.CharField(
        max_length=200, blank=True, verbose_name='ID suscripción externa'
    )
    external_reference = models.CharField(
        max_length=200, blank=True, verbose_name='referencia externa'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='actualizado')

    class Meta:
        verbose_name = 'suscripción'
        verbose_name_plural = 'suscripciones'
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.user} — {self.plan} ({self.get_status_display()})'
