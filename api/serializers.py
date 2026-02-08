"""
Serializers for the Store Management System API.

These serializers handle the conversion of model instances to JSON and vice versa.
"""
from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    Converts Customer instances to/from JSON representation.
    """
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'contact_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Validate that email is unique (except for the current instance on update)."""
        if self.instance:
            if Customer.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A customer with this email already exists.")
        else:
            if Customer.objects.filter(email=value).exists():
                raise serializers.ValidationError("A customer with this email already exists.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Converts Product instances to/from JSON representation.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        """Validate that price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock(self, value):
        """Validate that stock is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    Includes nested product information for better API responses.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'quantity', 'subtotal', 'created_at']
        read_only_fields = ['id', 'subtotal', 'created_at']

    def validate_quantity(self, value):
        """Validate that quantity is positive."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def validate(self, data):
        """Validate that product is in stock."""
        product = data.get('product')
        quantity = data.get('quantity')
        
        if product and quantity:
            if not product.is_in_stock(quantity):
                raise serializers.ValidationError(
                    f"Insufficient stock. Available: {product.stock}, Requested: {quantity}"
                )
        return data

    def get_subtotal(self, obj):
        """Calculate and return the subtotal for this order item."""
        return str(obj.get_subtotal())


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Order model with nested items.
    Used for retrieve and detail views.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'date_ordered', 'total_price', 'items', 'updated_at']
        read_only_fields = ['id', 'date_ordered', 'total_price', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    Converts Order instances to/from JSON representation.
    """
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'date_ordered', 'total_price', 'item_count', 'updated_at']
        read_only_fields = ['id', 'date_ordered', 'total_price', 'updated_at']

    def get_item_count(self, obj):
        """Return the number of items in the order."""
        return obj.items.count()
