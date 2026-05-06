# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests de ownership: ningún usuario puede acceder a datos de otro usuario.

Cubre:
- detail de colección ajena → 404
- edit de colección ajena → 404
- delete de colección ajena → 404
- item_create en colección ajena → 404
- item_edit de item ajeno → 404
- item_delete de item ajeno → 404
"""

import pytest
from django.urls import reverse

from apps.collections.models import Collection, CollectionItem
from apps.users.models import User


@pytest.fixture
def propietario(db):
    return User.objects.create_user(email='owner@example.com', password='Pass1234!')


@pytest.fixture
def intruso(db):
    return User.objects.create_user(email='intruder@example.com', password='Pass1234!')


@pytest.fixture
def coleccion(propietario):
    return Collection.objects.create(owner=propietario, name='Colección Privada')


@pytest.fixture
def item(coleccion):
    return CollectionItem.objects.create(collection=coleccion, name='Item Privado')


@pytest.fixture
def cliente_intruso(client, intruso):
    client.force_login(intruso)
    return client


@pytest.mark.django_db
class TestOwnershipColeccion:

    def test_detail_ajeno_404(self, cliente_intruso, coleccion):
        url = reverse('collections:collection_detail', kwargs={'slug': coleccion.slug})
        assert cliente_intruso.get(url).status_code == 404

    def test_edit_ajeno_404(self, cliente_intruso, coleccion):
        url = reverse('collections:collection_edit', kwargs={'slug': coleccion.slug})
        assert cliente_intruso.get(url).status_code == 404

    def test_delete_ajeno_404(self, cliente_intruso, coleccion):
        url = reverse('collections:collection_delete', kwargs={'slug': coleccion.slug})
        assert cliente_intruso.post(url).status_code == 404


@pytest.mark.django_db
class TestOwnershipItems:

    def test_item_create_coleccion_ajena_404(self, cliente_intruso, coleccion):
        url = reverse('collections:item_create', kwargs={'collection_slug': coleccion.slug})
        data = {
            'name': 'Hack', 'description': '', 'personal_comment': '',
            'status': 'owned', 'position': 0,
        }
        assert cliente_intruso.post(url, data).status_code == 404

    def test_item_edit_ajeno_404(self, cliente_intruso, coleccion, item):
        url = reverse('collections:item_edit', kwargs={
            'collection_slug': coleccion.slug, 'slug': item.slug,
        })
        assert cliente_intruso.get(url).status_code == 404

    def test_item_delete_ajeno_404(self, cliente_intruso, coleccion, item):
        url = reverse('collections:item_delete', kwargs={
            'collection_slug': coleccion.slug, 'slug': item.slug,
        })
        assert cliente_intruso.post(url).status_code == 404
