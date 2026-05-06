# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests del servicio user_can_use_groups.

Cubre:
- usuario sin suscripción → False
- usuario con suscripción activa en plan sin grupos → False
- usuario con suscripción activa en plan con grupos → True
- usuario con suscripción suspendida en plan con grupos → False
- usuario con suscripción cancelada en plan con grupos → False
- usuario staff sin suscripción → True
"""

import pytest

from apps.billing.models import Plan, Subscription
from apps.billing.services import user_can_use_groups
from apps.users.models import User


@pytest.fixture
def plan_free(db):
    return Plan.objects.create(
        code='free',
        name='Free',
        tier=Plan.Tier.FREE,
        can_use_groups=False,
    )


@pytest.fixture
def plan_premium(db):
    return Plan.objects.create(
        code='premium',
        name='Premium',
        tier=Plan.Tier.PREMIUM,
        can_use_groups=True,
    )


@pytest.fixture
def usuario_free(db):
    return User.objects.create_user(email='free@example.com', password='Pass1234!')


@pytest.fixture
def usuario_staff(db):
    return User.objects.create_user(
        email='staff@example.com', password='Pass1234!', is_staff=True
    )


@pytest.mark.django_db
class TestUserCanUseGroups:

    def test_sin_suscripcion_es_false(self, usuario_free):
        assert user_can_use_groups(usuario_free) is False

    def test_suscripcion_activa_plan_sin_grupos_es_false(self, usuario_free, plan_free):
        Subscription.objects.create(
            user=usuario_free,
            plan=plan_free,
            status=Subscription.Status.ACTIVE,
        )
        assert user_can_use_groups(usuario_free) is False

    def test_suscripcion_activa_plan_con_grupos_es_true(self, usuario_free, plan_premium):
        Subscription.objects.create(
            user=usuario_free,
            plan=plan_premium,
            status=Subscription.Status.ACTIVE,
        )
        assert user_can_use_groups(usuario_free) is True

    def test_suscripcion_suspendida_plan_premium_es_false(self, usuario_free, plan_premium):
        Subscription.objects.create(
            user=usuario_free,
            plan=plan_premium,
            status=Subscription.Status.SUSPENDED,
        )
        assert user_can_use_groups(usuario_free) is False

    def test_suscripcion_cancelada_plan_premium_es_false(self, usuario_free, plan_premium):
        Subscription.objects.create(
            user=usuario_free,
            plan=plan_premium,
            status=Subscription.Status.CANCELED,
        )
        assert user_can_use_groups(usuario_free) is False

    def test_staff_sin_suscripcion_es_true(self, usuario_staff):
        assert user_can_use_groups(usuario_staff) is True
