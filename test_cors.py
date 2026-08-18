#!/usr/bin/env python3
"""
Simple script to test CORS configuration
"""

import requests
import json

def test_cors():
    """Test CORS configuration with different origins"""
    
    # Test URLs
    base_url = "http://localhost:8000"  # Change this to your API server URL
    test_endpoints = [
        "/api/cors-test/",
        "/api/products/",
        "/api/categories/",
    ]
    
    # Test origins
    test_origins = [
        "https://kushnathayurveda.com",
        "https://www.kushnathayurveda.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    
    print("Testing CORS configuration...")
    print("=" * 50)
    
    for endpoint in test_endpoints:
        print(f"\nTesting endpoint: {endpoint}")
        print("-" * 30)
        
        for origin in test_origins:
            try:
                # Test OPTIONS request (preflight)
                headers = {
                    'Origin': origin,
                    'Access-Control-Request-Method': 'GET',
                    'Access-Control-Request-Headers': 'Content-Type, Authorization',
                }
                
                response = requests.options(f"{base_url}{endpoint}", headers=headers)
                
                print(f"Origin: {origin}")
                print(f"  OPTIONS Status: {response.status_code}")
                print(f"  Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
                print(f"  Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not set')}")
                print(f"  Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not set')}")
                
                # Test GET request
                headers = {'Origin': origin}
                response = requests.get(f"{base_url}{endpoint}", headers=headers)
                
                print(f"  GET Status: {response.status_code}")
                print(f"  GET Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
                
            except requests.exceptions.RequestException as e:
                print(f"  Error: {e}")
            
            print()

if __name__ == "__main__":
    test_cors()
