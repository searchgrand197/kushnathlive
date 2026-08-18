import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kushnath_dashboard.settings')
django.setup()

from dashboard.models import CustomerOrder

def debug_phone_query():
    print("🔍 Debugging phone number query...")
    
    try:
        # Get all orders
        orders = CustomerOrder.objects.all()
        
        if orders.exists():
            print(f"✅ Found {orders.count()} orders in database")
            print("\n" + "="*80)
            
            for order in orders:
                print(f"Order ID: {order.id}")
                print(f"Order Number: {order.order_number}")
                print(f"Customer Name: {order.customer_name}")
                print(f"Customer Phone (raw): '{order.customer_phone}'")
                print(f"Customer Phone (type): {type(order.customer_phone)}")
                print(f"Customer Phone (length): {len(str(order.customer_phone))}")
                print(f"Customer Email: {order.customer_email}")
                print("-" * 80)
            
            # Test the exact query that our view uses
            print("\n🔍 Testing the exact query from our view:")
            test_phone = "+918181818181"
            print(f"Searching for phone: '{test_phone}'")
            
            # Try the exact filter
            filtered_orders = CustomerOrder.objects.filter(customer_phone=test_phone)
            print(f"Filtered orders count: {filtered_orders.count()}")
            
            if filtered_orders.exists():
                print("✅ Found orders with exact match!")
                for order in filtered_orders:
                    print(f"  - Order {order.order_number}: {order.customer_name}")
            else:
                print("❌ No exact matches found")
                
                # Try without the + symbol
                test_phone_no_plus = "918181818181"
                print(f"\nTrying without + symbol: '{test_phone_no_plus}'")
                filtered_orders_no_plus = CustomerOrder.objects.filter(customer_phone=test_phone_no_plus)
                print(f"Filtered orders count (no +): {filtered_orders_no_plus.count()}")
                
                # Try with just the number
                test_phone_just_number = "8181818181"
                print(f"\nTrying just the number: '{test_phone_just_number}'")
                filtered_orders_just_number = CustomerOrder.objects.filter(customer_phone=test_phone_just_number)
                print(f"Filtered orders count (just number): {filtered_orders_just_number.count()}")
                
                # Try contains search
                print(f"\nTrying contains search for '8181818181'")
                filtered_orders_contains = CustomerOrder.objects.filter(customer_phone__contains="8181818181")
                print(f"Filtered orders count (contains): {filtered_orders_contains.count()}")
                
        else:
            print("❌ No orders found in the database")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_phone_query()



