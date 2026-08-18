import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kushnath_dashboard.settings')
django.setup()

from dashboard.models import CustomerOrder

def find_existing_orders():
    print("🔍 Searching for existing orders in the database...")
    
    try:
        orders = CustomerOrder.objects.all()
        
        if orders.exists():
            print(f"✅ Found {orders.count()} orders:")
            print("-" * 80)
            
            for order in orders:
                print(f"Order ID: {order.id}")
                print(f"Order Number: {order.order_number}")
                print(f"Customer Name: {order.customer_name}")
                print(f"Customer Phone: {order.customer_phone}")
                print(f"Customer Email: {order.customer_email}")
                print(f"Order Status: {order.order_status}")
                print(f"Payment Status: {order.payment_status}")
                print(f"Total Amount: ₹{order.final_total}")
                print(f"Items Count: {order.items.count()}")
                print("-" * 80)
        else:
            print("❌ No orders found in the database")
            print("\nTo test the frontend orders page, you need to:")
            print("1. Create an order through the checkout process")
            print("2. Or manually add an order through Django admin")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    find_existing_orders()



