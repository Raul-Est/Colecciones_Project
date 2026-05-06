# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from .validators import rename_cover, validate_cover


class Collection(models.Model):

    class Visibility(models.TextChoices):
        PRIVATE = 'private', 'Privada'
        PUBLIC = 'public', 'Pública'

    class Category(models.TextChoices):
        BOOKS = 'books', 'Libros'
        GAMES = 'games', 'Juegos'
        MUSIC = 'music', 'Música'
        FIGURES = 'figures', 'Figuras'
        OTHER = 'other', 'Otros'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name='propietario',
    )
    name = models.CharField(max_length=200, verbose_name='nombre')
    slug = models.SlugField(max_length=220, blank=True, verbose_name='slug')
    description = models.TextField(blank=True, verbose_name='descripción')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name='categoría',
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
        verbose_name='visibilidad',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'colección'
        verbose_name_plural = 'colecciones'
        constraints = [
            models.UniqueConstraint(fields=['owner', 'slug'], name='unique_collection_owner_slug')
        ]
        indexes = [
            models.Index(fields=['owner', '-created_at']),
        ]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.owner.email})'


class CollectionItem(models.Model):

    class Status(models.TextChoices):
        OWNED = 'owned', 'En posesión'
        WANTED = 'wanted', 'Deseado'
        SOLD = 'sold', 'Vendido'
        LENT = 'lent', 'Prestado'

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='colección',
    )
    name = models.CharField(max_length=200, verbose_name='nombre')
    slug = models.SlugField(max_length=220, blank=True, verbose_name='slug')
    description = models.TextField(blank=True, verbose_name='descripción')
    personal_comment = models.TextField(blank=True, verbose_name='comentario personal')
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OWNED,
        verbose_name='estado',
    )
    cover = models.ImageField(
        upload_to=rename_cover,
        validators=[validate_cover],
        null=True,
        blank=True,
        verbose_name='carátula',
    )
    position = models.PositiveIntegerField(default=0, verbose_name='posición')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'elemento'
        verbose_name_plural = 'elementos'
        indexes = [
            models.Index(fields=['collection', 'position']),
        ]
        ordering = ['position', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} → {self.collection.name}'
