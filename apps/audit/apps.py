# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.audit'
    verbose_name = 'Auditoría'

    def ready(self):
        # Conectar las signals al arrancar la app.
        # El import aquí evita importaciones circulares.
        import apps.audit.signals  # noqa: F401
