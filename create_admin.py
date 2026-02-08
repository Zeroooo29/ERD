#!/usr/bin/env python
"""
Script to create a superuser account for Django admin.
Credentials:
- Username: admin
- Password: admin123
- Email: admin@example.com
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if admin user already exists
if User.objects.filter(username='admin').exists():
    print("✅ Admin user already exists")
    print("Username: admin")
    print("Password: admin123")
else:
    # Create superuser
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Admin user created successfully!")
    print("\nAdmin Credentials:")
    print("=" * 40)
    print("Username: admin")
    print("Password: admin123")
    print("Email: admin@example.com")
    print("=" * 40)
    print("\nAccess admin at: http://127.0.0.1:8000/admin/")
