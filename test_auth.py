#!/usr/bin/env python
import requests
import json

def test_authentication_and_orders():
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 Testing Authentication and Orders API")
    print("=" * 50)
    
    # Test 1: Try to access orders without authentication
    print("\n1. Testing orders endpoint without authentication:")
    response = requests.get(f"{base_url}/my-orders/?customer_mobile=%2B918181818181")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    # Test 2: Try to authenticate with a test phone number
    print("\n2. Testing authentication:")
    auth_data = {
        "username": "+918181818181",
        "password": "+918181818181"
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
        print(f"Auth Response: {auth_response.text}")
        
        if auth_response.status_code == 200:
            auth_result = auth_response.json()
            access_token = auth_result.get('access')
            
            if access_token:
                print(f"\n3. Testing orders endpoint with authentication:")
                orders_response = requests.get(
                    f"{base_url}/my-orders/?customer_mobile=%2B918181818181",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                )
                print(f"Orders Status: {orders_response.status_code}")
                print(f"Orders Response: {orders_response.text[:500]}...")
            else:
                print("No access token received")
        else:
            print("Authentication failed")
            
    except Exception as e:
        print(f"Error during authentication: {e}")

if __name__ == "__main__":
    test_authentication_and_orders()

