# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Activa'
        SUSPENDED = 'suspended', 'Suspendida'
        PENDING = 'pending', 'Pendiente de verificación'
        DELETED = 'deleted', 'Eliminada'

    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='nombre')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='apellidos')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    account_status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
        verbose_name='estado de cuenta',
    )

    email_verified = models.BooleanField(default=False, verbose_name='email verificado')
    mfa_enabled = models.BooleanField(default=False, verbose_name='MFA habilitado')
    last_password_change = models.DateTimeField(
        null=True, blank=True, verbose_name='último cambio de contraseña'
    )

    date_joined = models.DateTimeField(default=timezone.now, verbose_name='fecha de alta')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email


class Profile(models.Model):

    class Language(models.TextChoices):
        ES = 'es', 'Español'
        EN = 'en', 'English'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='usuario',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='avatar',
    )
    timezone = models.CharField(
        max_length=50,
        default='Europe/Madrid',
        verbose_name='zona horaria',
    )
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.ES,
        verbose_name='idioma',
    )
    bio = models.TextField(blank=True, verbose_name='biografía')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return f'Perfil de {self.user.email}'
