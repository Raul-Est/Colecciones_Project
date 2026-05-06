# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.billing.services import user_can_use_groups

from . import selectors, services
from .forms import CollectionForm, CollectionGroupForm, CollectionItemForm
from .models import Collection, CollectionGroup
from .suggestions import GROUP_SUGGESTIONS

# ── Colecciones ───────────────────────────────────────────────────────────────

@login_required
def collection_list(request):
    collections = selectors.get_user_collections(request.user)
    return render(request, 'collections/collection_list.html', {'collections': collections})


@login_required
def collection_detail(request, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    groups = selectors.get_groups_for_collection(collection)
    ungrouped_items = selectors.get_ungrouped_items(collection)
    return render(request, 'collections/collection_detail.html', {
        'collection': collection,
        'groups': groups,
        'ungrouped_items': ungrouped_items,
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
    group_qs = CollectionGroup.objects.filter(collection=collection)
    initial = {}
    group_slug_param = request.GET.get('group')
    if group_slug_param:
        pre_group = group_qs.filter(slug=group_slug_param).first()
        if pre_group:
            initial['group'] = pre_group
    form = CollectionItemForm(
        request.POST or None,
        request.FILES or None,
        initial=initial or None,
    )
    form.fields['group'].queryset = group_qs
    if form.is_valid():
        item = services.create_item(collection, form)
        if item.group:
            return redirect(
                'collections:group_detail',
                slug=collection.slug,
                group_slug=item.group.slug,
            )
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
    form.fields['group'].queryset = CollectionGroup.objects.filter(collection=collection)
    if form.is_valid():
        services.update_item(item, form)
        if item.group:
            return redirect(
                'collections:group_detail',
                slug=collection.slug,
                group_slug=item.group.slug,
            )
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
        group = item.group
        item.delete()
        if group:
            return redirect(
                'collections:group_detail',
                slug=collection.slug,
                group_slug=group.slug,
            )
        return redirect('collections:collection_detail', slug=collection.slug)
    return render(request, 'collections/item_confirm_delete.html', {
        'object': item,
        'collection': collection,
    })


# ── Grupos ────────────────────────────────────────────────────────────────────

@login_required
def group_create(request, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    if not user_can_use_groups(request.user):
        messages.error(
            request,
            'La creación de grupos está disponible solo para usuarios premium.',
        )
        return redirect('collections:collection_detail', slug=collection.slug)
    suggestions = GROUP_SUGGESTIONS.get(collection.category, [])
    form = CollectionGroupForm(request.POST or None)
    if form.is_valid():
        group = services.create_group(collection, form)
        return redirect('collections:group_detail', slug=collection.slug, group_slug=group.slug)
    return render(request, 'collections/group_form.html', {
        'form': form,
        'collection': collection,
        'suggestions': suggestions,
        'title': 'Nuevo grupo',
    })


@login_required
def group_detail(request, slug, group_slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    group = get_object_or_404(CollectionGroup, collection=collection, slug=group_slug)
    owned = group.items.filter(status='owned').order_by('position', '-created_at')
    wanted = group.items.filter(status='wanted').order_by('position', '-created_at')
    return render(request, 'collections/group_detail.html', {
        'collection': collection,
        'group': group,
        'owned': owned,
        'wanted': wanted,
    })


@login_required
def group_edit(request, slug, group_slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    group = get_object_or_404(CollectionGroup, collection=collection, slug=group_slug)
    suggestions = GROUP_SUGGESTIONS.get(collection.category, [])
    form = CollectionGroupForm(request.POST or None, instance=group)
    if form.is_valid():
        services.update_group(group, form)
        return redirect('collections:group_detail', slug=collection.slug, group_slug=group.slug)
    return render(request, 'collections/group_form.html', {
        'form': form,
        'collection': collection,
        'suggestions': suggestions,
        'title': 'Editar grupo',
    })


@login_required
def group_delete(request, slug, group_slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    group = get_object_or_404(CollectionGroup, collection=collection, slug=group_slug)
    if request.method == 'POST':
        group.delete()
        return redirect('collections:collection_detail', slug=collection.slug)
    return render(request, 'collections/group_confirm_delete.html', {
        'object': group,
        'collection': collection,
    })


# ── Mover / copiar ─────────────────────────────────────────────────────────────

@login_required
def item_move(request, collection_slug, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=collection_slug)
    item = get_object_or_404(collection.items, slug=slug)
    user_collections = Collection.objects.filter(owner=request.user)

    if request.method == 'POST':
        target_collection_id = request.POST.get('target_collection')
        target_group_id = request.POST.get('target_group') or None
        confirmed = request.POST.get('confirmed') == '1'
        target_collection = get_object_or_404(
            Collection, owner=request.user, pk=target_collection_id
        )
        target_group = None
        if target_group_id:
            target_group = get_object_or_404(
                CollectionGroup, collection=target_collection, pk=target_group_id
            )
        if not confirmed and item.collection_id != target_collection.pk:
            conflicts = services.get_conflicts([item], target_collection)
            if conflicts:
                all_groups = (
                    CollectionGroup.objects.filter(collection__owner=request.user)
                    .select_related('collection')
                    .order_by('collection__name', 'position', 'name')
                )
                return render(request, 'collections/item_move.html', {
                    'collection': collection,
                    'item': item,
                    'user_collections': user_collections,
                    'all_groups': all_groups,
                    'conflicts': conflicts,
                    'target_collection_id': target_collection_id,
                    'target_group_id': target_group_id,
                })
        services.move_item(item, target_collection, target_group)
        return redirect('collections:collection_detail', slug=target_collection.slug)

    all_groups = (
        CollectionGroup.objects.filter(collection__owner=request.user)
        .select_related('collection')
        .order_by('collection__name', 'position', 'name')
    )
    return render(request, 'collections/item_move.html', {
        'collection': collection,
        'item': item,
        'user_collections': user_collections,
        'all_groups': all_groups,
    })


@login_required
def group_move(request, slug, group_slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    group = get_object_or_404(CollectionGroup, collection=collection, slug=group_slug)
    user_collections = Collection.objects.filter(owner=request.user).exclude(pk=collection.pk)

    if request.method == 'POST':
        target_collection_id = request.POST.get('target_collection')
        confirmed = request.POST.get('confirmed') == '1'
        target_collection = get_object_or_404(
            Collection, owner=request.user, pk=target_collection_id
        )
        if not confirmed:
            conflicts = services.get_conflicts(group.items.all(), target_collection)
            if conflicts:
                return render(request, 'collections/group_move.html', {
                    'collection': collection,
                    'group': group,
                    'user_collections': user_collections,
                    'conflicts': conflicts,
                    'target_collection_id': target_collection_id,
                })
        services.move_group(group, target_collection)
        return redirect('collections:collection_detail', slug=target_collection.slug)

    return render(request, 'collections/group_move.html', {
        'collection': collection,
        'group': group,
        'user_collections': user_collections,
    })


@login_required
def collection_transfer(request, slug):
    collection = get_object_or_404(Collection, owner=request.user, slug=slug)
    user_collections = Collection.objects.filter(owner=request.user).exclude(pk=collection.pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        target_collection_id = request.POST.get('target_collection')
        confirmed = request.POST.get('confirmed') == '1'
        target_collection = get_object_or_404(
            Collection, owner=request.user, pk=target_collection_id
        )
        if not confirmed:
            conflicts = services.get_conflicts(collection.items.all(), target_collection)
            if conflicts:
                return render(request, 'collections/collection_transfer.html', {
                    'collection': collection,
                    'user_collections': user_collections,
                    'conflicts': conflicts,
                    'target_collection_id': target_collection_id,
                    'selected_action': action,
                })
        if action == 'move':
            services.move_collection_content(collection, target_collection)
        elif action == 'copy':
            services.copy_collection_content(collection, target_collection)
        return redirect('collections:collection_detail', slug=target_collection.slug)

    return render(request, 'collections/collection_transfer.html', {
        'collection': collection,
        'user_collections': user_collections,
    })

