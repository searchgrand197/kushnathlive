#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kushnath_dashboard.settings')
django.setup()

from django.contrib.auth.models import User
from customer.models import Customer
from dashboard.models import CustomerOrder

def fix_orders_issue():
    print("🔧 Fixing Orders Display Issue")
    print("=" * 50)
    
    # Step 1: Check existing orders
    print("\n1. Checking existing orders...")
    total_orders = CustomerOrder.objects.count()
    print(f"   Total orders in database: {total_orders}")
    
    if total_orders > 0:
        sample_orders = CustomerOrder.objects.all()[:3]
        print("   Sample orders:")
        for order in sample_orders:
            print(f"     - Order #{order.order_number}: {order.customer_phone}")
    
    # Step 2: Check existing users
    print("\n2. Checking existing users...")
    total_users = User.objects.count()
    print(f"   Total users in database: {total_users}")
    
    # Step 3: Create or update test user
    print("\n3. Setting up test user...")
    phone_number = "+918181818181"
    
    # Create Django user
    user, created = User.objects.get_or_create(
        username=phone_number,
        defaults={
            'first_name': 'Shubham',
            'last_name': 'Garg',
            'email': 'shubham@example.com',
            'is_active': True
        }
    )
    
    if created:
        user.set_password(phone_number)
        user.save()
        print(f"   ✅ Created new user: {phone_number}")
    else:
        print(f"   ✅ User already exists: {phone_number}")
    
    # Create customer profile
    customer, customer_created = Customer.objects.get_or_create(
        user=user,
        defaults={
            'name': 'Shubham Garg',
            'email': 'shubham@example.com'
        }
    )
    
    if customer_created:
        print(f"   ✅ Created customer profile for: {customer.name}")
    else:
        print(f"   ✅ Customer profile already exists for: {customer.name}")
    
    # Step 4: Test the API logic
    print("\n4. Testing API logic...")
    orders = CustomerOrder.objects.filter(customer_phone=phone_number)
    print(f"   Orders found for {phone_number}: {orders.count()}")
    
    if orders.exists():
        print("   ✅ Orders found! The API should work correctly.")
        print("\n   📋 Order Summary:")
        for i, order in enumerate(orders[:3], 1):
            print(f"     {i}. Order #{order.order_number}")
            print(f"        Status: {order.order_status}")
            print(f"        Total: ₹{order.final_total}")
    else:
        print("   ❌ No orders found for this phone number")
    
    # Step 5: Instructions
    print("\n5. Next Steps:")
    print("   📱 Login to frontend with:")
    print(f"      Phone: {phone_number}")
    print(f"      Password: {phone_number}")
    print("   🔗 Go to: http://localhost:5173/login")
    print("   📋 After login, go to: http://localhost:5173/orders")
    print("   🐛 Use the debug component to test the API")

if __name__ == "__main__":
    fix_orders_issue()

