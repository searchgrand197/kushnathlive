import requests
import json

# Test the new customer orders endpoint
def test_customer_orders():
    base_url = "http://127.0.0.1:8000/api"
    
    # Use the actual phone number from the database
    test_mobile = "+918181818181"  # This phone number has orders in the database
    
    print(f"Testing customer orders endpoint for mobile: {test_mobile}")
    
    try:
        # Test the endpoint
        response = requests.get(f"{base_url}/my-orders/?customer_mobile={test_mobile}")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                orders = data.get('orders', [])
                print(f"\n✅ Success! Found {len(orders)} orders")
                
                for i, order in enumerate(orders):
                    print(f"\n--- Order {i+1} ---")
                    print(f"Order Number: {order.get('order_number')}")
                    print(f"Customer: {order.get('customer_name')}")
                    print(f"Status: {order.get('order_status')}")
                    print(f"Payment: {order.get('payment_status')}")
                    print(f"Total: ₹{order.get('final_total')}")
                    print(f"Items: {len(order.get('items', []))}")
            else:
                print(f"❌ API returned success: false")
                print(f"Message: {data.get('message')}")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_customer_orders()
