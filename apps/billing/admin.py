# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from django.contrib import admin

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'tier', 'is_active', 'sort_order',
        'can_use_groups', 'max_collections', 'max_items_total',
    ]
    list_filter = ['tier', 'is_active', 'can_use_groups']
    search_fields = ['code', 'name']
    ordering = ['sort_order', 'code']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'started_at', 'current_period_end', 'auto_renew']
    list_filter = ['status', 'plan__tier', 'auto_renew']
    search_fields = ['user__email', 'plan__code', 'provider_customer_id']
    ordering = ['-started_at']
    raw_id_fields = ['user']
