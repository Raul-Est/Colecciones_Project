# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib import admin

from .models import Collection, CollectionItem


class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 0
    fields = ['name', 'status', 'position', 'cover']
    readonly_fields = ['slug']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'visibility', 'created_at']
    list_filter = ['category', 'visibility']
    search_fields = ['name', 'owner__email']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    inlines = [CollectionItemInline]


@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'collection', 'status', 'position', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'collection__name', 'collection__owner__email']
    readonly_fields = ['slug', 'created_at', 'updated_at']
