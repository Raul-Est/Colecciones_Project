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
    # Elementos
    path('<slug:collection_slug>/items/nuevo/', views.item_create, name='item_create'),
    path('<slug:collection_slug>/items/<slug:slug>/editar/', views.item_edit, name='item_edit'),
    path(
        '<slug:collection_slug>/items/<slug:slug>/eliminar/',
        views.item_delete,
        name='item_delete',
    ),
]
