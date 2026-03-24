from django.contrib import admin

from .models import Category, Product, Shipment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'stock']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'tracking_number', 'user', 'product',
        'courier_company', 'status', 'estimated_delivery', 'updated_at',
    ]
    list_filter = ['status', 'courier_company']
    search_fields = ['tracking_number', 'user__email', 'product__name', 'courier_company']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['user', 'product']
