#!/usr/bin/env python
import requests
import json

def test_frontend_auth_flow():
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 Testing Frontend Authentication Flow")
    print("=" * 50)
    
    # Test phone number that has orders
    phone_number = "+918181818181"
    
    print(f"\n📱 Testing with phone: {phone_number}")
    
    # Step 1: Authenticate (simulate frontend login)
    print("\n1. Authenticating...")
    auth_data = {
        "username": phone_number,
        "password": phone_number
    }
    
    try:
        auth_response = requests.post(
            f"{base_url}/token/",
            headers={
                "Authorization": "Token 454efe120c467091556c613bada8af5b3bab3bc5",
                "Content-Type": "application/json"
            },
            json=auth_data
        )
        
        print(f"Auth Status: {auth_response.status_code}")
        
        if auth_response.status_code == 200:
            auth_result = auth_response.json()
            access_token = auth_result.get('access')
            user_data = auth_result.get('user')
            
            print(f"✅ Authentication successful!")
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   User: {user_data.get('username') if user_data else 'N/A'}")
            
            # Step 2: Get orders (simulate frontend orders request)
            print(f"\n2. Fetching orders...")
            orders_response = requests.get(
                f"{base_url}/my-orders/?customer_mobile={phone_number}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
            )
            
            print(f"Orders Status: {orders_response.status_code}")
            
            if orders_response.status_code == 200:
                orders_result = orders_response.json()
                orders = orders_result.get('orders', [])
                
                print(f"✅ Orders fetched successfully!")
                print(f"   Total Orders: {len(orders)}")
                
                if orders:
                    print(f"\n📋 Order Summary:")
                    for i, order in enumerate(orders[:3], 1):  # Show first 3 orders
                        print(f"   {i}. Order #{order.get('order_number')}")
                        print(f"      Status: {order.get('order_status')}")
                        print(f"      Total: ₹{order.get('final_total')}")
                        print(f"      Date: {order.get('created_at')[:10]}")
                else:
                    print("   ❌ No orders found")
            else:
                print(f"❌ Failed to fetch orders: {orders_response.text}")
                
        else:
            print(f"❌ Authentication failed: {auth_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_frontend_auth_flow()

