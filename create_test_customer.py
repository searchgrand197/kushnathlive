#!/usr/bin/env python3
"""
Script to create test customer for order API testing
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kushnath_dashboard.settings')
django.setup()

from django.contrib.auth.models import User
from customer.models import Customer, CustomerMobile
from dashboard.models import Category, Product
from cart.models import CartDetails, CartItem

def create_test_customer():
    """Create test customer with mobile number +918181818181"""
    print("Creating test customer...")
    
    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Superuser created: admin/admin123")
    
    # Create customer
    customer, created = Customer.objects.get_or_create(
        email='shubham@example.com',
        defaults={
            'name': 'Shubham Doe',
            'user': User.objects.first()
        }
    )
    if created:
        print("✓ Customer created")
    
    # Create customer mobile
    mobile, created = CustomerMobile.objects.get_or_create(
        customer=customer,
        mobile='+918181818181'
    )
    if created:
        print("✓ Customer mobile created")
    
    # Create category if not exists
    category, created = Category.objects.get_or_create(
        name='Ayurvedic Medicines',
        defaults={'description': 'Traditional Ayurvedic medicines'}
    )
    if created:
        print("✓ Category created")
    
    # Create products if not exist
    products_data = [
        {
            'name': 'Chyawanprash',
            'quantity': '500g',
            'sku': 'CHY001',
            'stock': 100,
            'price': 299.00,
            'description': 'Traditional Ayurvedic health supplement'
        },
        {
            'name': 'Ashwagandha',
            'quantity': '100g',
            'sku': 'ASH001',
            'stock': 50,
            'price': 199.00,
            'description': 'Natural stress relief supplement'
        }
    ]
    
    products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            sku=product_data['sku'],
            defaults={
                'name': product_data['name'],
                'quantity': product_data['quantity'],
                'category': category,
                'stock': product_data['stock'],
                'price': product_data['price'],
                'description': product_data['description'],
                'available': True
            }
        )
        products.append(product)
        if created:
            print(f"✓ Product created: {product.name}")
    
    # Create cart
    cart, created = CartDetails.objects.get_or_create(
        user=customer.user
    )
    if created:
        print("✓ Cart created")
    
    # Add items to cart
    for product in products:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        if created:
            print(f"✓ Added {product.name} to cart")
    
    print("\n=== Test Data Summary ===")
    print(f"Customer: {customer.name} ({customer.email})")
    print(f"Mobile: {mobile.mobile}")
    print(f"Cart ID: {cart.id}")
    print(f"Products in cart: {cart.items.count()}")
    
    print("\n=== Available Products ===")
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ₹{product.price}, Stock: {product.stock}")
    
    print("\n=== API Test Payloads ===")
    print("\n1. Cart-based order:")
    print(f"""{{
    "customer_mobile": "{mobile.mobile}",
    "cart_id": {cart.id},
    "payment_method": "cod",
    "delivery_pincode": "110001",
    "delivery_city": "New Delhi",
    "delivery_state": "Delhi",
    "delivery_country": "India",
    "delivery_address_text": "123 Test Street",
    "recipient_name": "Shubham Doe",
    "recipient_phone": "{mobile.mobile}",
    "notes": "Test order"
}}""")
    
    print("\n2. Direct items order:")
    print(f"""{{
    "customer_mobile": "{mobile.mobile}",
    "payment_method": "cod",
    "delivery_pincode": "110001",
    "delivery_city": "New Delhi",
    "delivery_state": "Delhi",
    "delivery_country": "India",
    "delivery_address_text": "123 Test Street",
    "recipient_name": "Shubham Doe",
    "recipient_phone": "{mobile.mobile}",
    "notes": "Test order",
    "order_items": [
        {{"product_id": {products[0].id}, "quantity": 2}},
        {{"product_id": {products[1].id}, "quantity": 1}}
    ]
}}""")
    
    print("\n=== Ready to Test ===")
    print("You can now use the above payloads to test the order API!")

if __name__ == "__main__":
    create_test_customer() 