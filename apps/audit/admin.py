# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'evento', 'email_usado', 'user', 'ip')
    list_filter = ('evento', 'timestamp')
    search_fields = ('email_usado', 'ip', 'user__email')
    readonly_fields = ('user', 'email_usado', 'evento', 'ip', 'timestamp')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
