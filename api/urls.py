"""
URL configuration for the API app.

Registers all ViewSets with routers to automatically generate URL patterns for CRUD operations.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    ProductViewSet,
    OrderViewSet,
    OrderItemViewSet,
)

# Create a router and register all viewsets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

# Include the router URLs
urlpatterns = [
    path('', include(router.urls)),
]
