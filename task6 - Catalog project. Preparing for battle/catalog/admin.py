from django.contrib import admin

from .models import SSD, Interface, FormFactor, Cart, CartItem


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


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "status", "created_at")
    list_filter = ("status", "created_at", "owner")
    inlines = [CartItemInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Менеджер видит только свои партии
        return qs.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        # Менеджер может менять только свои партии
        if obj is not None and not request.user.is_superuser:
            return obj.owner == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Менеджер может удалять только свои партии
        if obj is not None and not request.user.is_superuser:
            return obj.owner == request.user
        return super().has_delete_permission(request, obj)
