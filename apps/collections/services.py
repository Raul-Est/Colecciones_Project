# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.utils.text import slugify

from .models import CollectionGroup, CollectionItem

# ── Helpers de slug único ──────────────────────────────────────────────────────

def _unique_group_slug(base_slug, target_collection):
    qs = CollectionGroup.objects.filter(collection=target_collection)
    slug = base_slug
    n = 1
    while qs.filter(slug=slug).exists():
        slug = f'{base_slug}-{n}'
        n += 1
    return slug


def _unique_item_slug(base_slug, target_collection):
    qs = CollectionItem.objects.filter(collection=target_collection)
    slug = base_slug
    n = 1
    while qs.filter(slug=slug).exists():
        slug = f'{base_slug}-{n}'
        n += 1
    return slug


def create_collection(owner, form):
    collection = form.save(commit=False)
    collection.owner = owner
    collection.save()
    return collection


def update_collection(collection, form):
    collection = form.save(commit=False)
    collection.save()
    return collection


def create_item(collection, form):
    item = form.save(commit=False)
    item.collection = collection
    item.save()
    return item


def update_item(item, form):
    item = form.save(commit=False)
    item.save()
    return item


def create_group(collection, form):
    group = form.save(commit=False)
    group.collection = collection
    group.save()
    return group


def update_group(group, form):
    group = form.save(commit=False)
    group.save()
    return group


# ── Mover / copiar ─────────────────────────────────────────────────────────────

def _find_duplicate(name, collection, exclude_pk=None):
    """Devuelve el item con el mismo nombre en la colección, si existe."""
    qs = CollectionItem.objects.filter(collection=collection, name=name)
    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)
    return qs.first()


def get_conflicts(items, target_collection):
    """
    Devuelve lista de (item_origen, item_existente) para los items cuyo nombre
    ya existe en target_collection.
    """
    result = []
    for item in items:
        existing = _find_duplicate(item.name, target_collection, exclude_pk=item.pk)
        if existing:
            result.append((item, existing))
    return result


def move_item(item, target_collection, target_group=None):
    """
    Mueve un elemento a otra colección / grupo.
    Si ya existe un elemento con el mismo nombre en la colección destino,
    se fusionan sumando cantidades y el original se elimina.
    """
    if item.collection_id != target_collection.pk:
        existing = _find_duplicate(item.name, target_collection, exclude_pk=item.pk)
        if existing:
            existing.quantity += item.quantity
            existing.save()
            item.delete()
            return existing
        item.slug = _unique_item_slug(item.slug, target_collection)
        item.collection = target_collection
    item.group = target_group
    item.save()
    return item


def move_group(group, target_collection):
    """
    Mueve un grupo con todos sus elementos a otra colección.
    Los items duplicados (mismo nombre) se fusionan con los existentes en destino.
    """
    for item in list(group.items.all()):
        existing = _find_duplicate(item.name, target_collection)
        if existing:
            existing.quantity += item.quantity
            existing.save()
            item.delete()
        else:
            item.slug = _unique_item_slug(item.slug, target_collection)
            item.collection = target_collection
            item.save()
    group.slug = _unique_group_slug(group.slug, target_collection)
    group.collection = target_collection
    group.save()
    return group


def move_collection_content(source_collection, target_collection):
    """Mueve todos los grupos y elementos de source a target. Source queda vacío."""
    for group in list(source_collection.groups.all()):
        move_group(group, target_collection)
    for item in list(source_collection.items.filter(group__isnull=True)):
        move_item(item, target_collection, None)


def copy_collection_content(source_collection, target_collection):
    """
    Copia todos los grupos y elementos de source a target.
    Si ya existe un item con el mismo nombre en destino, suma cantidades.
    Source no cambia.
    """
    group_map = {}
    for group in source_collection.groups.all():
        new_slug = _unique_group_slug(slugify(group.name) or 'grupo', target_collection)
        new_group = CollectionGroup(
            collection=target_collection,
            name=group.name,
            slug=new_slug,
            description=group.description,
            position=group.position,
        )
        new_group.save()
        group_map[group.pk] = new_group
    for item in source_collection.items.all():
        dest_group = group_map.get(item.group_id)
        existing = _find_duplicate(item.name, target_collection)
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            new_slug = _unique_item_slug(slugify(item.name) or 'elemento', target_collection)
            CollectionItem(
                collection=target_collection,
                group=dest_group,
                name=item.name,
                slug=new_slug,
                description=item.description,
                personal_comment=item.personal_comment,
                status=item.status,
                cover=item.cover,
                quantity=item.quantity,
                position=item.position,
            ).save()

