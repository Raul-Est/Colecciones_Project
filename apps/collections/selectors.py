# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from .models import Collection, CollectionGroup, CollectionItem


def get_user_collections(user):
    return Collection.objects.filter(owner=user).order_by('-created_at')


def get_collection_for_user(user, slug):
    return Collection.objects.filter(owner=user, slug=slug).first()


def get_items_for_collection(collection):
    return CollectionItem.objects.filter(collection=collection).order_by('position', '-created_at')


def get_ungrouped_items(collection):
    return CollectionItem.objects.filter(
        collection=collection, group__isnull=True
    ).order_by('position', '-created_at')


def get_item_for_collection(collection, slug):
    return CollectionItem.objects.filter(collection=collection, slug=slug).first()


def get_groups_for_collection(collection):
    return CollectionGroup.objects.filter(collection=collection).order_by('position', 'name')


def get_group_for_collection(collection, slug):
    return CollectionGroup.objects.filter(collection=collection, slug=slug).first()

