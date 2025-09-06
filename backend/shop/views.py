from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Product, CartItem
from .serializers import ProductSerializer, CartSerializer, OrderSerializer
from .utils import get_or_create_cart, compute_shipping, create_order_from_cart
from django.views.decorators.csrf import ensure_csrf_cookie

class ProductList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        qs = Product.objects.filter(is_active=True)
        return Response(ProductSerializer(qs, many=True).data)

class CartDetail(APIView):
    permission_classes = [AllowAny]  # carrito también para invitados (con CSRF en POST)
    def get(self, request):
        cart = get_or_create_cart(request)
        return Response(CartSerializer(cart).data)

class CartAddItem(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        cart = get_or_create_cart(request)
        pid = request.data.get("product_id")
        qty = int(request.data.get("qty", 1))
        if not pid or qty < 1:
            return Response({"detail": "invalid_payload"}, status=400)
        product = get_object_or_404(Product, pk=pid, is_active=True)
        item, created = cart.items.get_or_create(
            product=product,
            defaults={"qty": qty, "unit_price": product.price}
        )
        if not created:
            item.qty += qty
            item.save(update_fields=["qty"])
        return Response({"detail": "added", "cart": CartSerializer(cart).data}, status=201)

class CartUpdateItem(APIView):
    permission_classes = [AllowAny]
    def patch(self, request, item_id: int):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        qty = int(request.data.get("qty", 1))
        if qty < 1:
            item.delete()
            return Response({"detail": "removed", "cart": CartSerializer(cart).data})
        item.qty = qty
        item.save(update_fields=["qty"])
        return Response({"detail": "updated", "cart": CartSerializer(cart).data})

class CartRemoveItem(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, item_id: int):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        item.delete()
        return Response({"detail": "removed", "cart": CartSerializer(cart).data})

class CheckoutSummary(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        cart = get_or_create_cart(request)
        s = CartSerializer(cart).data
        s["shipping"] = str(compute_shipping(cart))
        s["total"] = str(cart.items.all() and (cart.items.aggregate_total if False else (sum(i["subtotal"] for i in s["items"]) + float(s["shipping"]))) )
        # Nota: arriba total lo calculamos nuevamente; puedes simplificar si tu CartSerializer ya trae total.
        return Response({"cart": s})

class CheckoutConfirm(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Requiere CSRF y cookies (como todo POST)
        required = ["email","full_name","address","city"]
        for k in required:
            if not (request.data.get(k) or "").strip():
                return Response({"detail": f"missing:{k}"}, status=400)
        try:
            order = create_order_from_cart(request, request.data)
        except ValueError as e:
            msg = str(e)
            if msg.startswith("no_stock:"):
                pid = msg.split(":")[1]
                return Response({"detail": "no_stock", "product_id": pid}, status=400)
            if msg == "empty_cart":
                return Response({"detail": "empty_cart"}, status=400)
            return Response({"detail": "invalid"}, status=400)
        return Response({"detail": "created", "order": OrderSerializer(order).data}, status=201)