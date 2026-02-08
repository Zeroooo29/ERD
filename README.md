# Store Management System - Django REST Framework

A comprehensive REST API for managing a store system with Customers, Orders, and Products. Built with Django REST Framework with full CRUD functionality and business logic validation.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Business Logic](#business-logic)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Bonus Features](#bonus-features)

## ✨ Features

- ✅ Full CRUD operations for Customers, Products, Orders, and OrderItems
- ✅ Automatic order total price calculation
- ✅ Stock validation and availability checking
- ✅ Prevent ordering out-of-stock products
- ✅ RESTful API with browsable interface
- ✅ Pagination and filtering support
- ✅ Search functionality
- ✅ Admin dashboard for easy management
- ✅ Well-documented API with examples
- ✅ Input validation and error handling

## 📁 Project Structure

```
store_system/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database (created after migration)
├── store_system/                # Main project package
│   ├── __init__.py
│   ├── settings.py              # Project settings and configuration
│   ├── urls.py                  # Main URL router
│   ├── asgi.py                  # ASGI configuration
│   └── wsgi.py                  # WSGI configuration
├── api/                         # API app package
│   ├── __init__.py
│   ├── models.py                # Database models (Customer, Product, Order, OrderItem)
│   ├── serializers.py           # DRF serializers for API responses
│   ├── views.py                 # ViewSets for CRUD operations
│   ├── urls.py                  # API URL configuration
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   └── migrations/              # Database migrations
└── README.md                    # This file
```

## 📦 Requirements

- Python 3.10 or higher
- Django 4.2+
- Django REST Framework
- python-decouple (optional, for environment variables)

## 🚀 Installation & Setup

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install django djangorestframework
```

Optional (for better development experience):
```bash
pip install django-filter python-decouple
```

### Step 3: Navigate to Project

```bash
cd store_system
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

## ▶️ Running the Server

Start the development server:

```bash
python manage.py runserver
```

The server will be available at:
- **API Base URL:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **Browsable API:** http://localhost:8000/api/customers/ (or other endpoints)

## 🌐 API Endpoints

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers/` | List all customers (paginated) |
| POST | `/api/customers/` | Create new customer |
| GET | `/api/customers/<id>/` | Retrieve specific customer |
| PUT | `/api/customers/<id>/` | Update customer |
| DELETE | `/api/customers/<id>/` | Delete customer |
| GET | `/api/customers/<id>/orders/` | Get all orders for a customer |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products (paginated) |
| POST | `/api/products/` | Create new product |
| GET | `/api/products/<id>/` | Retrieve specific product |
| PUT | `/api/products/<id>/` | Update product |
| DELETE | `/api/products/<id>/` | Delete product |
| GET | `/api/products/in_stock/` | Get all in-stock products |
| GET | `/api/products/out_of_stock/` | Get all out-of-stock products |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List all orders (paginated) |
| POST | `/api/orders/` | Create new order |
| GET | `/api/orders/<id>/` | Retrieve specific order with items |
| PUT | `/api/orders/<id>/` | Update order |
| DELETE | `/api/orders/<id>/` | Delete order |
| POST | `/api/orders/<id>/add_item/` | Add product to order |
| POST | `/api/orders/<id>/remove_item/` | Remove product from order |
| GET | `/api/orders/by_customer/?customer_id=<id>` | Get orders by customer |

### Order Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/order-items/` | List all order items (paginated) |
| POST | `/api/order-items/` | Create new order item |
| GET | `/api/order-items/<id>/` | Retrieve specific order item |
| PUT | `/api/order-items/<id>/` | Update order item |
| DELETE | `/api/order-items/<id>/` | Delete order item |

## 📝 Examples

### 1. Create a Customer

**Request:**
```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "contact_number": "+1-555-0001"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "contact_number": "+1-555-0001",
  "created_at": "2026-02-08T10:30:00Z",
  "updated_at": "2026-02-08T10:30:00Z"
}
```

### 2. Create a Product

**Request:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": "999.99",
    "stock": 50
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Laptop",
  "price": "999.99",
  "stock": 50,
  "created_at": "2026-02-08T10:35:00Z",
  "updated_at": "2026-02-08T10:35:00Z"
}
```

### 3. Create an Order

**Request:**
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": 1
  }'
```

**Response:**
```json
{
  "id": 1,
  "customer": 1,
  "customer_name": "John Doe",
  "date_ordered": "2026-02-08T10:40:00Z",
  "total_price": "0.00",
  "item_count": 0,
  "updated_at": "2026-02-08T10:40:00Z"
}
```

### 4. Add Product to Order

**Request:**
```bash
curl -X POST http://localhost:8000/api/orders/1/add_item/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity": 2
  }'
```

**Response:**
```json
{
  "id": 1,
  "customer": 1,
  "customer_name": "John Doe",
  "date_ordered": "2026-02-08T10:40:00Z",
  "total_price": "1999.98",
  "items": [
    {
      "id": 1,
      "order": 1,
      "product": 1,
      "product_name": "Laptop",
      "product_price": "999.99",
      "quantity": 2,
      "subtotal": "1999.98",
      "created_at": "2026-02-08T10:45:00Z"
    }
  ],
  "updated_at": "2026-02-08T10:45:00Z"
}
```

### 5. Get Order Details

**Request:**
```bash
curl http://localhost:8000/api/orders/1/
```

**Response:**
```json
{
  "id": 1,
  "customer": 1,
  "customer_name": "John Doe",
  "date_ordered": "2026-02-08T10:40:00Z",
  "total_price": "1999.98",
  "items": [
    {
      "id": 1,
      "order": 1,
      "product": 1,
      "product_name": "Laptop",
      "product_price": "999.99",
      "quantity": 2,
      "subtotal": "1999.98",
      "created_at": "2026-02-08T10:45:00Z"
    }
  ],
  "updated_at": "2026-02-08T10:45:00Z"
}
```

### 6. Update Product

**Request:**
```bash
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "price": "1299.99",
    "stock": 40
  }'
```

### 7. Delete Order Item

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/orders/1/remove_item/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1
  }'
```

## 🔒 Business Logic

### Automatic Total Price Calculation
- When an order item is added, updated, or removed, the order's total price is automatically calculated
- Total price = Sum of (Product Price × Quantity) for all items in the order

### Stock Validation
- When adding items to an order, the system checks if sufficient stock is available
- Returns an error if requesting more than available stock
- Prevents ordering out-of-stock products

### Data Integrity
- Unique constraint on customer email to prevent duplicates
- Foreign key relationships ensure referential integrity
- OrderItem unique constraint prevents duplicate products in the same order

## 🧪 Testing

### Using Django Browsable API

1. Navigate to http://localhost:8000/api/
2. Use the web interface to test endpoints
3. Fill in forms to create/update records
4. Click "GET", "POST", "PUT", "DELETE" buttons

### Using cURL

See examples above for cURL commands.

### Using Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the endpoints listed above
3. Set request type (GET, POST, etc.)
4. Add JSON body for POST/PUT requests
5. Send and view responses

### Using Thunder Client (VS Code)

1. Install Thunder Client extension in VS Code
2. Create requests using the endpoints above
3. Test CRUD operations

## 💻 Technologies Used

- **Django** - Web framework
- **Django REST Framework** - REST API framework
- **SQLite** - Database (default, can be changed to PostgreSQL/MySQL)
- **Python** - Programming language

## 🌟 Bonus Features Implemented

### 1. Pagination
- Products and Customers list are paginated (10 items per page)
- Configure in `settings.py` using `REST_FRAMEWORK` settings

### 2. Search & Filter
- Search customers by name, email, or contact number
- Filter products by price
- Filter orders by customer
- Filter order items by product or order

### 3. Admin Dashboard Customization
- Customized list displays with relevant fields
- Search functionality in admin
- Inline editing of OrderItems within Orders
- Readonly timestamps for audit trail
- Organized fieldsets for better UX

### 4. Custom Actions
- **Get customer's orders:** `GET /api/customers/<id>/orders/`
- **Get in-stock products:** `GET /api/products/in_stock/`
- **Get out-of-stock products:** `GET /api/products/out_of_stock/`
- **Add items to order:** `POST /api/orders/<id>/add_item/`
- **Remove items from order:** `POST /api/orders/<id>/remove_item/`
- **Filter orders by customer:** `GET /api/orders/by_customer/?customer_id=<id>`

### 5. Comprehensive Validation
- Email uniqueness validation
- Price and stock non-negative validation
- Stock availability checking before adding to order
- Quantity validation
- Helpful error messages

## 📖 Database Models

### Customer
```
id (Primary Key)
name (CharField)
email (EmailField, unique)
contact_number (CharField)
created_at (DateTimeField)
updated_at (DateTimeField)
```

### Product
```
id (Primary Key)
name (CharField)
price (DecimalField)
stock (IntegerField)
created_at (DateTimeField)
updated_at (DateTimeField)
```

### Order
```
id (Primary Key)
customer (ForeignKey -> Customer)
date_ordered (DateTimeField)
total_price (DecimalField, auto-calculated)
updated_at (DateTimeField)
```

### OrderItem
```
id (Primary Key)
order (ForeignKey -> Order)
product (ForeignKey -> Product)
quantity (IntegerField)
created_at (DateTimeField)
unique_together: (order, product)
```

## 🔐 Security Notes

⚠️ **For Production:**
- Change `DEBUG = False` in settings.py
- Set a secure `SECRET_KEY`
- Use environment variables for sensitive data
- Use a production database (PostgreSQL/MySQL)
- Configure `ALLOWED_HOSTS` properly
- Enable CSRF protection
- Use HTTPS

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/)

## 🤝 Support

For issues or questions:
1. Check the Admin panel at `/admin/`
2. Review error messages in the API responses
3. Verify all data requirements are met
4. Check the database migrations have been applied

## 📄 License

This project is open source and available for educational purposes.

---

**Happy coding!** 🚀
