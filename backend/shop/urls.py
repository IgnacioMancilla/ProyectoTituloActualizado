from django.urls import path
from .views import (
    ProductList, CartDetail, CartAddItem, CartUpdateItem, CartRemoveItem,
    CheckoutSummary, CheckoutConfirm
)

urlpatterns = [
    path("products/", ProductList.as_view()),
    path("cart/", CartDetail.as_view()),
    path("cart/items/", CartAddItem.as_view()),
    path("cart/items/<int:item_id>/", CartUpdateItem.as_view()),
    path("cart/items/<int:item_id>/delete/", CartRemoveItem.as_view()),
    path("checkout/summary/", CheckoutSummary.as_view()),
    path("checkout/confirm/", CheckoutConfirm.as_view()),
]
