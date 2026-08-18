#!/usr/bin/env python
import requests
import json

def debug_api_call():
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 Debugging API Call")
    print("=" * 50)
    
    # Test phone number
    phone_number = "+918181818181"
    
    # First, get an access token
    print("1. Getting access token...")
    auth_data = {
        "username": phone_number,
        "password": phone_number
    }
    
    auth_response = requests.post(
        f"{base_url}/token/",
        headers={
            "Authorization": "Token 454efe120c467091556c613bada8af5b3bab3bc5",
            "Content-Type": "application/json"
        },
        json=auth_data
    )
    
    if auth_response.status_code != 200:
        print(f"❌ Auth failed: {auth_response.text}")
        return
    
    auth_result = auth_response.json()
    access_token = auth_result.get('access')
    
    print(f"✅ Got access token: {access_token[:20]}...")
    
    # Now test the orders endpoint
    print(f"\n2. Testing orders endpoint...")
    print(f"   URL: {base_url}/my-orders/?customer_mobile={phone_number}")
    print(f"   Headers: Authorization: Bearer {access_token[:20]}...")
    
    orders_response = requests.get(
        f"{base_url}/my-orders/?customer_mobile={phone_number}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"\n3. Response:")
    print(f"   Status: {orders_response.status_code}")
    print(f"   Headers: {dict(orders_response.headers)}")
    print(f"   Content: {orders_response.text[:1000]}...")
    
    if orders_response.status_code == 200:
        try:
            result = orders_response.json()
            orders = result.get('orders', [])
            print(f"\n4. Parsed Result:")
            print(f"   Success: {result.get('success')}")
            print(f"   Orders Count: {len(orders)}")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if orders:
                print(f"\n5. First Order:")
                first_order = orders[0]
                print(f"   Order Number: {first_order.get('order_number')}")
                print(f"   Customer: {first_order.get('customer_name')}")
                print(f"   Phone: {first_order.get('customer_mobile')}")
                print(f"   Status: {first_order.get('order_status')}")
            else:
                print(f"\n5. No orders found in response")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
    else:
        print(f"❌ Request failed with status {orders_response.status_code}")

if __name__ == "__main__":
    debug_api_call()

