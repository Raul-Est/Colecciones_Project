# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from . import selectors, services
from .forms import CollectionForm, CollectionItemForm
from .models import Collection

# ── Colecciones ───────────────────────────────────────────────────────────────

@login_required
def collection_list(request):
    collections = selectors.get_user_collections(request.user)
    return render(request, 'collections/collection_list.html', {'collections': collections})


@login_required
def collection_detail(request, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    items = selectors.get_items_for_collection(collection)
    return render(request, 'collections/collection_detail.html', {
        'collection': collection,
        'items': items,
    })


@login_required
def collection_create(request):
    form = CollectionForm(request.POST or None)
    if form.is_valid():
        collection = services.create_collection(request.user, form)
        return redirect('collections:collection_detail', slug=collection.slug)
    ctx = {'form': form, 'title': 'Nueva colección'}
    return render(request, 'collections/collection_form.html', ctx)


@login_required
def collection_edit(request, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    form = CollectionForm(request.POST or None, instance=collection)
    if form.is_valid():
        services.update_collection(collection, form)
        return redirect('collections:collection_detail', slug=collection.slug)
    ctx = {'form': form, 'title': 'Editar colección'}
    return render(request, 'collections/collection_form.html', ctx)


@login_required
def collection_delete(request, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    if request.method == 'POST':
        collection.delete()
        return redirect('collections:collection_list')
    return render(request, 'collections/collection_confirm_delete.html', {'object': collection})


# ── Elementos ─────────────────────────────────────────────────────────────────

@login_required
def item_create(request, collection_slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=collection_slug)
    form = CollectionItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        services.create_item(collection, form)
        return redirect('collections:collection_detail', slug=collection.slug)
    return render(request, 'collections/item_form.html', {
        'form': form,
        'collection': collection,
        'title': 'Añadir elemento',
    })


@login_required
def item_edit(request, collection_slug, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=collection_slug)
    item = get_object_or_404(collection.items, slug=slug)
    form = CollectionItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        services.update_item(item, form)
        return redirect('collections:collection_detail', slug=collection.slug)
    return render(request, 'collections/item_form.html', {
        'form': form,
        'collection': collection,
        'title': 'Editar elemento',
    })


@login_required
def item_delete(request, collection_slug, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=collection_slug)
    item = get_object_or_404(collection.items, slug=slug)
    if request.method == 'POST':
        item.delete()
        return redirect('collections:collection_detail', slug=collection.slug)
    return render(request, 'collections/item_confirm_delete.html', {
        'object': item,
        'collection': collection,
    })

