# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests de permisos y grupos base.

Cubre:
- los tres grupos (free, premium, staff) existen en BD tras la migración
"""

import pytest
from django.contrib.auth.models import Group


@pytest.mark.django_db
class TestGruposBase:

    def test_grupo_free_existe(self):
        assert Group.objects.filter(name='free').exists()

    def test_grupo_premium_existe(self):
        assert Group.objects.filter(name='premium').exists()

    def test_grupo_staff_existe(self):
        assert Group.objects.filter(name='staff').exists()
