# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests de los modelos Collection y CollectionItem.

Cubre:
- creación básica de Collection
- slug se genera automáticamente desde el nombre
- unicidad de (owner, slug)
- creación de CollectionItem
- slug de item generado automáticamente
- __str__ de ambos modelos
"""

import pytest
from django.db import IntegrityError

from apps.collections.models import Collection, CollectionItem
from apps.users.models import User


@pytest.fixture
def usuario(db):
    return User.objects.create_user(email='col@example.com', password='Pass1234!')


@pytest.fixture
def otra_usuario(db):
    return User.objects.create_user(email='otro@example.com', password='Pass1234!')


@pytest.fixture
def coleccion(usuario):
    return Collection.objects.create(owner=usuario, name='Mis Libros')


@pytest.mark.django_db
class TestCollectionModel:

    def test_crear_coleccion(self, usuario):
        col = Collection.objects.create(owner=usuario, name='Mis Juegos')
        assert col.pk is not None
        assert col.name == 'Mis Juegos'

    def test_slug_generado_automaticamente(self, usuario):
        col = Collection.objects.create(owner=usuario, name='Mis Libros Favoritos')
        assert col.slug == 'mis-libros-favoritos'

    def test_valores_por_defecto(self, usuario):
        col = Collection.objects.create(owner=usuario, name='Test')
        assert col.visibility == Collection.Visibility.PRIVATE
        assert col.category == Collection.Category.OTHER

    def test_str(self, coleccion, usuario):
        assert str(coleccion) == f'Mis Libros ({usuario.email})'

    def test_unicidad_owner_slug(self, usuario):
        Collection.objects.create(owner=usuario, name='Duplicado', slug='duplicado')
        with pytest.raises(IntegrityError):
            Collection.objects.create(owner=usuario, name='Duplicado 2', slug='duplicado')

    def test_mismo_slug_distinto_owner(self, usuario, otra_usuario):
        Collection.objects.create(owner=usuario, name='Compartida', slug='compartida')
        col2 = Collection.objects.create(owner=otra_usuario, name='Compartida', slug='compartida')
        assert col2.pk is not None


@pytest.mark.django_db
class TestCollectionItemModel:

    def test_crear_item(self, coleccion):
        item = CollectionItem.objects.create(collection=coleccion, name='Libro 1')
        assert item.pk is not None
        assert item.collection == coleccion

    def test_slug_item_generado(self, coleccion):
        item = CollectionItem.objects.create(collection=coleccion, name='El Señor de los Anillos')
        assert item.slug == 'el-senor-de-los-anillos'

    def test_estado_por_defecto(self, coleccion):
        item = CollectionItem.objects.create(collection=coleccion, name='Item Test')
        assert item.status == CollectionItem.Status.OWNED

    def test_str(self, coleccion):
        item = CollectionItem.objects.create(collection=coleccion, name='Dune')
        assert str(item) == 'Dune → Mis Libros'

    def test_posicion_por_defecto(self, coleccion):
        item = CollectionItem.objects.create(collection=coleccion, name='Item')
        assert item.position == 0
