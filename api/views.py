"""
API Views for the Store Management System.

Implements ViewSets for CRUD operations on Customers, Products, Orders, and OrderItems.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Customer, Product, Order, OrderItem
from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderDetailSerializer,
    OrderItemSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer CRUD operations.
    
    Endpoints:
    - GET /api/customers/ - List all customers
    - POST /api/customers/ - Create new customer
    - GET /api/customers/<id>/ - Retrieve specific customer
    - PUT /api/customers/<id>/ - Update customer
    - DELETE /api/customers/<id>/ - Delete customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email']
    search_fields = ['name', 'email', 'contact_number']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """
        Custom action to get all orders for a specific customer.
        
        Endpoint: GET /api/customers/<id>/orders/
        """
        customer = self.get_object()
        orders = customer.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product CRUD operations.
    
    Endpoints:
    - GET /api/products/ - List all products
    - POST /api/products/ - Create new product
    - GET /api/products/<id>/ - Retrieve specific product
    - PUT /api/products/<id>/ - Update product
    - DELETE /api/products/<id>/ - Delete product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name']
    ordering_fields = ['price', 'stock', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """
        Custom action to get all products currently in stock.
        
        Endpoint: GET /api/products/in_stock/
        """
        products = self.queryset.filter(stock__gt=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """
        Custom action to get all out-of-stock products.
        
        Endpoint: GET /api/products/out_of_stock/
        """
        products = self.queryset.filter(stock=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrderItem CRUD operations.
    
    Endpoints:
    - GET /api/order-items/ - List all order items
    - POST /api/order-items/ - Create new order item
    - GET /api/order-items/<id>/ - Retrieve specific order item
    - PUT /api/order-items/<id>/ - Update order item
    - DELETE /api/order-items/<id>/ - Delete order item
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order', 'product']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """
        Override create to automatically update order total price.
        """
        order_item = serializer.save()
        order_item.order.calculate_total_price()

    def perform_update(self, serializer):
        """
        Override update to automatically update order total price.
        """
        order_item = serializer.save()
        order_item.order.calculate_total_price()

    def perform_destroy(self, instance):
        """
        Override destroy to automatically update order total price.
        """
        order = instance.order
        instance.delete()
        order.calculate_total_price()


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order CRUD operations.
    
    Endpoints:
    - GET /api/orders/ - List all orders
    - POST /api/orders/ - Create new order
    - GET /api/orders/<id>/ - Retrieve specific order
    - PUT /api/orders/<id>/ - Update order
    - DELETE /api/orders/<id>/ - Delete order
    - POST /api/orders/<id>/add_item/ - Add item to order
    - DELETE /api/orders/<id>/remove_item/ - Remove item from order
    """
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer']
    ordering_fields = ['date_ordered', 'total_price']
    ordering = ['-date_ordered']

    def get_serializer_class(self):
        """
        Use detailed serializer for retrieve (detail view),
        standard serializer for list and other operations.
        """
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """
        Override create to calculate initial total price.
        """
        order = serializer.save()
        order.calculate_total_price()

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        Custom action to add a product to an order.
        
        Endpoint: POST /api/orders/<id>/add_item/
        Expected JSON: {"product": <product_id>, "quantity": <quantity>}
        """
        order = self.get_object()
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response(
                {'error': 'Both product and quantity are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {'error': 'Quantity must be greater than 0.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Quantity must be a valid integer.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, pk=product_id)

        # Check stock availability
        if not product.is_in_stock(quantity):
            return Response(
                {
                    'error': f'Insufficient stock. Available: {product.stock}, Requested: {quantity}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add or update order item
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # If item already exists, update quantity
            old_quantity = order_item.quantity
            order_item.quantity += quantity
            if not product.is_in_stock(order_item.quantity):
                order_item.quantity = old_quantity  # Rollback
                return Response(
                    {
                        'error': f'Insufficient stock. Available: {product.stock}, Current: {old_quantity}'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            order_item.save()

        # Update order total price
        order.calculate_total_price()

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """
        Custom action to remove a product from an order.
        
        Endpoint: POST /api/orders/<id>/remove_item/
        Expected JSON: {"product": <product_id>}
        """
        order = self.get_object()
        product_id = request.data.get('product')

        if not product_id:
            return Response(
                {'error': 'Product ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_item = get_object_or_404(OrderItem, order=order, product_id=product_id)
        order_item.delete()

        # Update order total price
        order.calculate_total_price()

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """
        Custom action to filter orders by customer.
        
        Endpoint: GET /api/orders/by_customer/?customer_id=<id>
        """
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response(
                {'error': 'customer_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        orders = self.queryset.filter(customer_id=customer_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
