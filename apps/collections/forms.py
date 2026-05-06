# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django import forms

from .models import Collection, CollectionItem


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description', 'category', 'visibility']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'category': 'Categoría',
            'visibility': 'Visibilidad',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CollectionItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = ['name', 'description', 'personal_comment', 'status', 'cover', 'position']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'personal_comment': 'Comentario personal',
            'status': 'Estado',
            'cover': 'Carátula',
            'position': 'Posición',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'personal_comment': forms.Textarea(attrs={'rows': 3}),
        }

