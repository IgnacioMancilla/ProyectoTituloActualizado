from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product, ProductImage, Order
from .serializers import ProductAdminSerializer, ProductImageSerializer, OrderAdminSerializer

class ProductAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductAdminSerializer

class ProductMainImageUpload(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, pk: int):
        product = get_object_or_404(Product, pk=pk)
        file = request.FILES.get("image")
        if not file:
            return Response({"detail":"missing_file"}, status=400)
        product.image = file
        product.save(update_fields=["image"])
        return Response(ProductAdminSerializer(product).data, status=200)

class ProductGalleryUpload(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, pk: int):
        product = get_object_or_404(Product, pk=pk)
        file = request.FILES.get("image")
        if not file:
            return Response({"detail":"missing_file"}, status=400)
        img = ProductImage.objects.create(product=product, image=file)
        return Response(ProductImageSerializer(img).data, status=201)

class ProductGalleryDelete(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, img_id: int):
        img = get_object_or_404(ProductImage, pk=img_id)
        img.delete()
        return Response({"detail":"deleted"})

class OrderAdminViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderAdminSerializer

from rest_framework.decorators import action

class OrderStatusUpdate(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get("status")
        if status_value not in ["pending","paid","cancelled"]:
            return Response({"detail":"invalid_status"}, status=400)
        order.status = status_value
        order.save(update_fields=["status"])
        return Response(OrderAdminSerializer(order).data)
