# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.urls import path

from . import views

app_name = 'collections'

urlpatterns = [
    # Colecciones
    path('', views.collection_list, name='collection_list'),
    path('nueva/', views.collection_create, name='collection_create'),
    path('<slug:slug>/', views.collection_detail, name='collection_detail'),
    path('<slug:slug>/editar/', views.collection_edit, name='collection_edit'),
    path('<slug:slug>/eliminar/', views.collection_delete, name='collection_delete'),
    path('<slug:slug>/transferir/', views.collection_transfer, name='collection_transfer'),
    # Grupos
    path('<slug:slug>/grupos/nuevo/', views.group_create, name='group_create'),
    path('<slug:slug>/grupos/<slug:group_slug>/', views.group_detail, name='group_detail'),
    path('<slug:slug>/grupos/<slug:group_slug>/editar/', views.group_edit, name='group_edit'),
    path(
        '<slug:slug>/grupos/<slug:group_slug>/eliminar/',
        views.group_delete,
        name='group_delete',
    ),
    path(
        '<slug:slug>/grupos/<slug:group_slug>/mover/',
        views.group_move,
        name='group_move',
    ),
    # Elementos
    path('<slug:collection_slug>/items/nuevo/', views.item_create, name='item_create'),
    path('<slug:collection_slug>/items/<slug:slug>/editar/', views.item_edit, name='item_edit'),
    path(
        '<slug:collection_slug>/items/<slug:slug>/eliminar/',
        views.item_delete,
        name='item_delete',
    ),
    path(
        '<slug:collection_slug>/items/<slug:slug>/mover/',
        views.item_move,
        name='item_move',
    ),
]
