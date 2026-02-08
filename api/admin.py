"""
Django Admin configuration for the Store Management System.

Registers all models and customizes their admin interface.
"""
from django.contrib import admin
from .models import Customer, Product, Order, OrderItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model."""
    list_display = ['name', 'email', 'contact_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'contact_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at', 'price']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product Details', {
            'fields': ('name', 'price', 'stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem to allow editing items within Order."""
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity']
    readonly_fields = []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ['id', 'customer', 'date_ordered', 'total_price']
    list_filter = ['date_ordered', 'customer']
    search_fields = ['customer__name', 'id']
    readonly_fields = ['date_ordered', 'total_price', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('date_ordered', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Override save to recalculate total price."""
        super().save_model(request, obj, form, change)
        obj.calculate_total_price()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""
    list_display = ['order', 'product', 'quantity', 'get_subtotal']
    list_filter = ['created_at', 'order__customer']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['created_at']

    def get_subtotal(self, obj):
        """Display subtotal in list view."""
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'
