# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Migración de datos: crea los grupos base del sistema.

- free:    usuarios con plan gratuito (por defecto al registrarse)
- premium: usuarios con plan de pago
- staff:   operadores internos con acceso ampliado
"""

from django.db import migrations

GRUPOS = ['free', 'premium', 'staff']


def crear_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for nombre in GRUPOS:
        Group.objects.get_or_create(name=nombre)


def eliminar_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=GRUPOS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(crear_grupos, reverse_code=eliminar_grupos),
    ]
