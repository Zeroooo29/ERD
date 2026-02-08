"""
Database models for the Store Management System.

Models:
- Customer: Stores customer information
- Product: Stores product details with pricing and stock
- Order: Represents an order placed by a customer
- OrderItem: Join table linking orders to products with quantity
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from decimal import Decimal


class Customer(models.Model):
    """
    Customer model to store customer information.
    
    Fields:
    - name: Customer's full name
    - email: Customer's email address
    - contact_number: Customer's phone number
    """
    name = models.CharField(max_length=255, help_text="Customer's full name")
    email = models.EmailField(unique=True, help_text="Customer's email address")
    contact_number = models.CharField(max_length=20, help_text="Customer's contact number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Customers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"


class Product(models.Model):
    """
    Product model to store product information.
    
    Fields:
    - name: Product name
    - price: Product price
    - stock: Available quantity in stock
    """
    name = models.CharField(max_length=255, help_text="Product name")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Product price"
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Available quantity in stock"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"

    def is_in_stock(self, quantity=1):
        """Check if the requested quantity is available in stock."""
        return self.stock >= quantity


class Order(models.Model):
    """
    Order model representing an order placed by a customer.
    
    Fields:
    - customer: ForeignKey to Customer
    - date_ordered: Date and time when order was placed
    - total_price: Automatically calculated total price of the order
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="Customer who placed the order"
    )
    date_ordered = models.DateTimeField(auto_now_add=True, help_text="Order placement date")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total price of the order"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-date_ordered']

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} ({self.total_price})"

    def calculate_total_price(self):
        """Calculate and update the total price based on order items."""
        total = self.items.aggregate(
            total=Sum(F('product__price') * F('quantity'), output_field=models.DecimalField())
        )['total'] or Decimal('0')
        self.total_price = total
        self.save()
        return self.total_price


class OrderItem(models.Model):
    """
    OrderItem (Join Table) model linking orders to products with quantity.
    
    Fields:
    - order: ForeignKey to Order
    - product: ForeignKey to Product
    - quantity: Quantity of the product in this order
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Order this item belongs to"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        help_text="Product in the order"
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of the product"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (Order #{self.order.id})"

    def get_subtotal(self):
        """Calculate subtotal for this order item."""
        return self.product.price * self.quantity
