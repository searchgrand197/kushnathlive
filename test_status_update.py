import requests
import json

# Test the order status update API
url = "http://127.0.0.1:8000/api/order-management/8/order-status/"
data = {"order_status": "processing"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.patch(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
    else:
        print(f"Error: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")



