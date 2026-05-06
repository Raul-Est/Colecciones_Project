# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests de las vistas CRUD de colecciones y elementos.

Cubre:
- list: usuario autenticado ve sus colecciones
- detail: usuario ve detalle de su colección
- create: GET muestra formulario, POST crea colección
- edit: GET muestra formulario, POST actualiza colección
- delete: POST elimina colección
- item_create: POST añade elemento a colección
- item_edit: POST actualiza elemento
- item_delete: POST elimina elemento
- usuario no autenticado redirige a login
"""

import pytest
from django.urls import reverse

from apps.billing.models import Plan, Subscription
from apps.collections.models import Collection, CollectionItem
from apps.users.models import User


@pytest.fixture
def usuario(db):
    return User.objects.create_user(email='views@example.com', password='Pass1234!')


@pytest.fixture
def coleccion(usuario):
    return Collection.objects.create(owner=usuario, name='Mi Colección')


@pytest.fixture
def item(coleccion):
    return CollectionItem.objects.create(collection=coleccion, name='Elemento 1')


@pytest.fixture
def cliente_auth(client, usuario):
    client.force_login(usuario)
    return client


@pytest.mark.django_db
class TestCollectionListView:

    def test_get_autenticado(self, cliente_auth, coleccion):
        url = reverse('collections:collection_list')
        response = cliente_auth.get(url)
        assert response.status_code == 200
        assert 'Mi Colección'.encode() in response.content

    def test_get_anonimo_redirige(self, client):
        url = reverse('collections:collection_list')
        response = client.get(url)
        assert response.status_code == 302
        assert '/account/login/' in response['Location']


@pytest.mark.django_db
class TestCollectionDetailView:

    def test_get_owner(self, cliente_auth, coleccion):
        url = reverse('collections:collection_detail', kwargs={'slug': coleccion.slug})
        response = cliente_auth.get(url)
        assert response.status_code == 200

    def test_get_otro_usuario_404(self, client, db, coleccion):
        otro = User.objects.create_user(email='otro@example.com', password='Pass1234!')
        client.force_login(otro)
        url = reverse('collections:collection_detail', kwargs={'slug': coleccion.slug})
        response = client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestCollectionCreateView:

    def test_get(self, cliente_auth):
        url = reverse('collections:collection_create')
        response = cliente_auth.get(url)
        assert response.status_code == 200

    def test_post_crea_coleccion(self, cliente_auth, usuario):
        url = reverse('collections:collection_create')
        data = {'name': 'Nueva', 'description': '', 'category': 'books', 'visibility': 'private'}
        response = cliente_auth.post(url, data)
        assert response.status_code == 302
        assert Collection.objects.filter(owner=usuario, name='Nueva').exists()


@pytest.mark.django_db
class TestCollectionEditView:

    def test_post_actualiza(self, cliente_auth, coleccion):
        url = reverse('collections:collection_edit', kwargs={'slug': coleccion.slug})
        data = {
            'name': 'Renombrada', 'description': '', 'category': 'games', 'visibility': 'public',
        }
        response = cliente_auth.post(url, data)
        assert response.status_code == 302
        coleccion.refresh_from_db()
        assert coleccion.name == 'Renombrada'


@pytest.mark.django_db
class TestCollectionDeleteView:

    def test_post_elimina(self, cliente_auth, coleccion):
        url = reverse('collections:collection_delete', kwargs={'slug': coleccion.slug})
        response = cliente_auth.post(url)
        assert response.status_code == 302
        assert not Collection.objects.filter(pk=coleccion.pk).exists()


@pytest.mark.django_db
class TestItemCreateView:

    def test_post_crea_item(self, cliente_auth, coleccion):
        url = reverse('collections:item_create', kwargs={'collection_slug': coleccion.slug})
        data = {
            'name': 'Nuevo Item', 'description': '', 'personal_comment': '',
            'status': 'owned', 'position': 0,
        }
        response = cliente_auth.post(url, data)
        assert response.status_code == 302
        assert CollectionItem.objects.filter(collection=coleccion, name='Nuevo Item').exists()


@pytest.mark.django_db
class TestItemEditView:

    def test_post_actualiza_item(self, cliente_auth, coleccion, item):
        url = reverse('collections:item_edit', kwargs={
            'collection_slug': coleccion.slug, 'slug': item.slug,
        })
        data = {
            'name': 'Editado', 'description': '', 'personal_comment': '',
            'status': 'wanted', 'position': 1,
        }
        response = cliente_auth.post(url, data)
        assert response.status_code == 302
        item.refresh_from_db()
        assert item.name == 'Editado'


@pytest.mark.django_db
class TestItemDeleteView:

    def test_post_elimina_item(self, cliente_auth, coleccion, item):
        url = reverse('collections:item_delete', kwargs={
            'collection_slug': coleccion.slug, 'slug': item.slug,
        })
        response = cliente_auth.post(url)
        assert response.status_code == 302
        assert not CollectionItem.objects.filter(pk=item.pk).exists()


# ── Gate premium en group_create ──────────────────────────────────────────────

@pytest.fixture
def plan_premium(db):
    return Plan.objects.create(
        code='premium',
        name='Premium',
        tier=Plan.Tier.PREMIUM,
        can_use_groups=True,
    )


@pytest.mark.django_db
class TestGroupCreateGate:

    def test_usuario_free_no_puede_crear_grupo(self, cliente_auth, coleccion):
        """Un usuario sin suscripción premium es redirigido con mensaje de error."""
        url = reverse('collections:group_create', kwargs={'slug': coleccion.slug})
        response = cliente_auth.get(url)
        assert response.status_code == 302
        assert response['Location'] == reverse(
            'collections:collection_detail', kwargs={'slug': coleccion.slug}
        )

    def test_usuario_premium_puede_ver_formulario(self, cliente_auth, coleccion, usuario,
                                                   plan_premium):
        """Un usuario con suscripción activa premium ve el formulario de creación de grupo."""
        Subscription.objects.create(
            user=usuario,
            plan=plan_premium,
            status=Subscription.Status.ACTIVE,
        )
        url = reverse('collections:group_create', kwargs={'slug': coleccion.slug})
        response = cliente_auth.get(url)
        assert response.status_code == 200

    def test_usuario_free_post_no_crea_grupo(self, cliente_auth, coleccion):
        """Un POST de usuario free tampoco crea el grupo."""
        from apps.collections.models import CollectionGroup
        url = reverse('collections:group_create', kwargs={'slug': coleccion.slug})
        response = cliente_auth.post(url, data={'name': 'Grupo X'})
        assert response.status_code == 302
        assert not CollectionGroup.objects.filter(collection=coleccion).exists()
