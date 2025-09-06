from django.contrib import admin
from .models import Product, ProductImage, Cart, CartItem, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProductImage)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "qty", "unit_price", "subtotal")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "email", "total", "status", "created_at")
    inlines = [OrderItemInline]
