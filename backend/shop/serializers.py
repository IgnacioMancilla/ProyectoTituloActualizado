from rest_framework import serializers
from .models import Product, ProductImage, Cart, CartItem, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "stock", "is_active"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]

class ProductAdminSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id","name","slug","price","stock","is_active","image","images"]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ["id", "product", "qty", "unit_price", "subtotal"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "items", "total"]

    def get_total(self, obj):
        return sum((i.subtotal for i in obj.items.all()), 0)
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "qty", "unit_price", "subtotal"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = [
            "id","number","status","email","full_name","phone","address","city","region","notes",
            "subtotal","shipping","total","created_at","items"
        ]

class OrderAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id","number","status","email","full_name","phone","address","city","region",
                  "notes","subtotal","shipping","total","created_at","items"]