#!/usr/bin/env python3
"""
Test script for Order API functionality
"""

import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000/api"
TOKEN = "your_jwt_token_here"  # Replace with actual token

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def test_create_order():
    """Test order creation"""
    print("Testing Order Creation...")
    
    order_data = {
        "customer_mobile": "9876543210",
        "cart_id": 1,
        "delivery_address_id": 1,
        "payment_method": "prepaid",
        "recipient_name": "Test Customer",
        "recipient_phone": "9876543210",
        "notes": "Test order for API verification"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            order = response.json()
            print(f"Order created successfully!")
            print(f"Order ID: {order['order_id']}")
            print(f"Status: {order['status']}")
            print(f"Total Amount: {order['total_amount']}")
            return order['id']
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_get_orders():
    """Test getting all orders"""
    print("\nTesting Get All Orders...")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            orders = response.json()
            print(f"Total orders: {len(orders['results'] if 'results' in orders else orders)}")
            return orders
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_get_orders_by_customer():
    """Test getting orders by customer mobile"""
    print("\nTesting Get Orders by Customer...")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/orders_by_customer/?customer_mobile=9876543210", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            orders = response.json()
            print(f"Orders for customer: {len(orders)}")
            return orders
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_update_order_status(order_id):
    """Test updating order status"""
    print(f"\nTesting Update Order Status for Order {order_id}...")
    
    status_data = {
        "new_status": "confirmed",
        "notes": "Order confirmed by test script"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/orders/{order_id}/update_status/", json=status_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            order = response.json()
            print(f"Order status updated to: {order['status']}")
            return order
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_create_shipment(order_id):
    """Test creating shipment"""
    print(f"\nTesting Create Shipment for Order {order_id}...")
    
    try:
        response = requests.post(f"{BASE_URL}/orders/{order_id}/create_shipment/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            order = response.json()
            print(f"Shipment created: {order['shipment_created']}")
            if order.get('tracking_number'):
                print(f"Tracking Number: {order['tracking_number']}")
            return order
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_dashboard_stats():
    """Test dashboard statistics"""
    print("\nTesting Dashboard Statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/orders/dashboard_stats/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print("Dashboard Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            return stats
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_filter_orders():
    """Test order filtering"""
    print("\nTesting Order Filtering...")
    
    # Test different filters
    filters = [
        "?status=pending",
        "?payment_method=prepaid",
        "?ordering=-created_at",
        "?search=test"
    ]
    
    for filter_param in filters:
        try:
            response = requests.get(f"{BASE_URL}/orders/{filter_param}", headers=headers)
            print(f"Filter: {filter_param}")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                orders = response.json()
                count = len(orders['results'] if 'results' in orders else orders)
                print(f"Results: {count} orders")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")

def main():
    """Main test function"""
    print("=== Order API Test Script ===")
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 50)
    
    # Test dashboard stats first
    test_dashboard_stats()
    
    # Test getting orders
    test_get_orders()
    
    # Test customer-specific orders
    test_get_orders_by_customer()
    
    # Test order filtering
    test_filter_orders()
    
    # Note: Order creation test requires valid cart and customer data
    print("\nNote: Order creation test requires:")
    print("- Valid JWT token")
    print("- Existing customer with mobile number")
    print("- Existing cart with items")
    print("- Existing delivery address")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main() 