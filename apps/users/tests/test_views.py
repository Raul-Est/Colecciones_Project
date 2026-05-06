# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests de las vistas de autenticación.

Cubre:
- GET register devuelve 200
- POST register con datos válidos crea user, crea perfil y redirige
- POST register con email duplicado devuelve error
- GET login devuelve 200
- POST login correcto redirige al dashboard
- POST login incorrecto devuelve 200 con error
- POST logout cierra sesión y redirige
- GET dashboard sin autenticar redirige al login
- GET dashboard autenticado devuelve 200
"""

import pytest

from apps.users.models import Profile, User

REGISTER_URL = '/account/register/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
DASHBOARD_URL = '/account/dashboard/'


@pytest.fixture
def usuario(db):
    user = User.objects.create_user(email='existing@example.com', password='Pass1234!')
    Profile.objects.create(user=user)
    return user


@pytest.mark.django_db
class TestRegisterView:

    def test_get_devuelve_200(self, client):
        response = client.get(REGISTER_URL)
        assert response.status_code == 200

    def test_registro_valido_crea_usuario(self, client):
        client.post(REGISTER_URL, {
            'email': 'nuevo@example.com',
            'password1': 'Segura1234!',
            'password2': 'Segura1234!',
        })
        assert User.objects.filter(email='nuevo@example.com').exists()

    def test_registro_valido_crea_perfil(self, client):
        client.post(REGISTER_URL, {
            'email': 'nuevo@example.com',
            'password1': 'Segura1234!',
            'password2': 'Segura1234!',
        })
        user = User.objects.get(email='nuevo@example.com')
        assert Profile.objects.filter(user=user).exists()

    def test_registro_valido_redirige(self, client):
        response = client.post(REGISTER_URL, {
            'email': 'nuevo@example.com',
            'password1': 'Segura1234!',
            'password2': 'Segura1234!',
        })
        assert response.status_code == 302

    def test_email_duplicado_devuelve_200_con_error(self, client, usuario):
        response = client.post(REGISTER_URL, {
            'email': 'existing@example.com',
            'password1': 'Segura1234!',
            'password2': 'Segura1234!',
        })
        assert response.status_code == 200
        assert User.objects.filter(email='existing@example.com').count() == 1

    def test_usuario_autenticado_redirige(self, client, usuario):
        client.force_login(usuario)
        response = client.get(REGISTER_URL)
        assert response.status_code == 302


@pytest.mark.django_db
class TestLoginView:

    def test_get_devuelve_200(self, client):
        response = client.get(LOGIN_URL)
        assert response.status_code == 200

    def test_login_correcto_redirige(self, client, usuario):
        response = client.post(LOGIN_URL, {
            'username': 'existing@example.com',
            'password': 'Pass1234!',
        })
        assert response.status_code == 302

    def test_login_incorrecto_devuelve_200(self, client, usuario):
        response = client.post(LOGIN_URL, {
            'username': 'existing@example.com',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200

    def test_usuario_autenticado_redirige(self, client, usuario):
        client.force_login(usuario)
        response = client.get(LOGIN_URL)
        assert response.status_code == 302


@pytest.mark.django_db
class TestLogoutView:

    def test_logout_post_redirige(self, client, usuario):
        client.force_login(usuario)
        response = client.post(LOGOUT_URL)
        assert response.status_code == 302

    def test_logout_cierra_sesion(self, client, usuario):
        client.force_login(usuario)
        client.post(LOGOUT_URL)
        response = client.get(DASHBOARD_URL)
        assert response.status_code == 302  # redirige al login porque no está autenticado

    def test_logout_get_redirige_sin_cerrar(self, client, usuario):
        client.force_login(usuario)
        response = client.get(LOGOUT_URL)
        assert response.status_code == 302


@pytest.mark.django_db
class TestDashboardView:

    def test_anonimo_redirige_al_login(self, client):
        response = client.get(DASHBOARD_URL)
        assert response.status_code == 302
        assert '/login/' in response['Location']

    def test_autenticado_devuelve_200(self, client, usuario):
        client.force_login(usuario)
        response = client.get(DASHBOARD_URL)
        assert response.status_code == 200
