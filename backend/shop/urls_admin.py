from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_admin import (
    ProductAdminViewSet, ProductMainImageUpload, ProductGalleryUpload, ProductGalleryDelete,
    OrderAdminViewSet, OrderStatusUpdate
)

router = DefaultRouter()
router.register(r'admin/products', ProductAdminViewSet, basename='admin-products')
router.register(r'admin/orders', OrderAdminViewSet, basename='admin-orders')

urlpatterns = [
    path("", include(router.urls)),
    path("admin/products/<int:pk>/upload-main/", ProductMainImageUpload.as_view()),
    path("admin/products/<int:pk>/gallery/", ProductGalleryUpload.as_view()),
    path("admin/products/gallery/<int:img_id>/delete/", ProductGalleryDelete.as_view()),
    path("admin/orders/<int:pk>/status/", OrderStatusUpdate.as_view()),
]
