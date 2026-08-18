#!/usr/bin/env python
import requests
import json

def test_no_auth():
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 Testing API without authentication")
    print("=" * 50)
    
    # Test phone number
    phone_number = "+918181818181"
    
    # Test the orders endpoint without authentication
    print(f"Testing orders endpoint without auth...")
    print(f"URL: {base_url}/my-orders/?customer_mobile={phone_number}")
    
    orders_response = requests.get(
        f"{base_url}/my-orders/?customer_mobile={phone_number}"
    )
    
    print(f"Status: {orders_response.status_code}")
    print(f"Response: {orders_response.text[:500]}...")
    
    if orders_response.status_code == 200:
        try:
            result = orders_response.json()
            orders = result.get('orders', [])
            print(f"Orders found: {len(orders)}")
            if orders:
                print(f"First order: {orders[0].get('order_number')}")
        except:
            print("Could not parse JSON response")

if __name__ == "__main__":
    test_no_auth()

