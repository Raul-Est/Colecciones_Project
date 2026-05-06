# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests del modelo User y Profile.

Cubre:
- crear usuario normal
- crear superusuario
- email vacío lanza ValueError
- valores por defecto del modelo
- get_full_name y get_short_name
- Profile se crea y relaciona con User
"""

import pytest

from apps.users.models import Profile, User


@pytest.mark.django_db
class TestUserManager:

    def test_crear_usuario_normal(self):
        user = User.objects.create_user(email='test@example.com', password='Pass1234!')
        assert user.pk is not None
        assert user.email == 'test@example.com'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_email_se_normaliza(self):
        user = User.objects.create_user(email='TEST@Example.COM', password='Pass1234!')
        assert user.email == 'TEST@example.com'

    def test_email_vacio_lanza_error(self):
        with pytest.raises(ValueError, match='El email es obligatorio'):
            User.objects.create_user(email='', password='Pass1234!')

    def test_crear_superusuario(self):
        user = User.objects.create_superuser(email='admin@example.com', password='Admin1234!')
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_superusuario_sin_is_staff_lanza_error(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='Admin1234!',
                is_staff=False,
            )


@pytest.mark.django_db
class TestUserModel:

    def test_str_devuelve_email(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        assert str(user) == 'u@example.com'

    def test_estado_por_defecto_es_active(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        assert user.account_status == User.AccountStatus.ACTIVE

    def test_email_verified_por_defecto_false(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        assert user.email_verified is False

    def test_get_full_name_con_nombre_y_apellido(self):
        user = User(email='u@example.com', first_name='Ana', last_name='García')
        assert user.get_full_name() == 'Ana García'

    def test_get_full_name_sin_datos_devuelve_email(self):
        user = User(email='u@example.com')
        assert user.get_full_name() == 'u@example.com'

    def test_get_short_name_con_nombre(self):
        user = User(email='u@example.com', first_name='Ana')
        assert user.get_short_name() == 'Ana'

    def test_get_short_name_sin_nombre_devuelve_email(self):
        user = User(email='u@example.com')
        assert user.get_short_name() == 'u@example.com'

    def test_username_field_es_email(self):
        assert User.USERNAME_FIELD == 'email'


@pytest.mark.django_db
class TestProfileModel:

    def test_crear_perfil(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        profile = Profile.objects.create(user=user)
        assert profile.pk is not None
        assert profile.user == user

    def test_str_perfil(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        profile = Profile.objects.create(user=user)
        assert str(profile) == 'Perfil de u@example.com'

    def test_valores_por_defecto(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        profile = Profile.objects.create(user=user)
        assert profile.timezone == 'Europe/Madrid'
        assert profile.language == Profile.Language.ES

    def test_relacion_inversa(self):
        user = User.objects.create_user(email='u@example.com', password='Pass1234!')
        profile = Profile.objects.create(user=user)
        assert user.profile == profile
