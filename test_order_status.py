import requests
import json

# Test the order status update endpoint
url = "http://127.0.0.1:8000/api/dashboard/orders/8/order-status/"
data = {"order_status": "confirmed"}

try:
    response = requests.patch(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Content: {response.text[:500]}...")  # First 500 chars
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            print(f"JSON Response: {json_response}")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
    else:
        print(f"Error Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")


