# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django import forms

from .models import Collection, CollectionGroup, CollectionItem


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


class CollectionGroupForm(forms.ModelForm):
    class Meta:
        model = CollectionGroup
        fields = ['name', 'description', 'position']
        labels = {
            'name': 'Nombre del grupo',
            'description': 'Descripción',
            'position': 'Posición',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class CollectionItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = [
            'name', 'description', 'personal_comment',
            'status', 'cover', 'quantity', 'position', 'group',
        ]
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'personal_comment': 'Comentario personal',
            'status': 'Estado',
            'cover': 'Carátula',
            'quantity': 'Cantidad',
            'position': 'Posición',
            'group': 'Grupo',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'personal_comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].required = False

    def clean_quantity(self):
        value = self.cleaned_data.get('quantity')
        return value if value is not None else 1

