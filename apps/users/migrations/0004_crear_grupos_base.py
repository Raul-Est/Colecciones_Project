# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.db import migrations


def crear_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for nombre in ('free', 'premium', 'staff'):
        Group.objects.get_or_create(name=nombre)


def eliminar_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=('free', 'premium', 'staff')).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_grupos_base'),
    ]

    operations = [
        migrations.RunPython(crear_grupos, eliminar_grupos),
    ]
