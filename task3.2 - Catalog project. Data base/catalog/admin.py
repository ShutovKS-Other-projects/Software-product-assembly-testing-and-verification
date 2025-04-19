from django.contrib import admin

from .models import SSD, Interface, FormFactor


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FormFactor)
class FormFactorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(SSD)
class SSDAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'sku', 'price', 'in_stock')
    list_filter = ('interface', 'form_factor', 'in_stock')
    search_fields = ('brand', 'model', 'sku')
    fieldsets = (
        ('Основное', {
            'fields': ('sku', 'brand', 'model', 'price')
        }),
        ('Характеристики', {
            'fields': ('capacity_gb', 'interface', 'form_factor')
        }),
        ('Дополнительно', {
            'fields': ('warranty_years', 'in_stock')
        }),
    )
