import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_login_existing_user():
    """Test login with existing user"""
    print("=== Testing Login with Existing User ===")
    
    # First, let's try to register a new user
    register_data = {
        "username": "testuser@example.com",
        "password": "testpass123",
        "name": "Test User",
        "email": "testuser@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=register_data)
    print(f"Registration Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # Now try to login with the same credentials
    login_data = {
        "username": "testuser@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=login_data)
    print(f"Login Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_register_new_user():
    """Test registration with new user"""
    print("=== Testing Registration with New User ===")
    
    register_data = {
        "username": "newuser@example.com",
        "password": "newpass123",
        "name": "New User",
        "email": "newuser@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=register_data)
    print(f"Registration Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_invalid_credentials():
    """Test with invalid credentials"""
    print("=== Testing Invalid Credentials ===")
    
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=login_data)
    print(f"Invalid Login Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_missing_fields():
    """Test with missing required fields"""
    print("=== Testing Missing Fields ===")
    
    # Test missing password
    data = {
        "username": "test@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=data)
    print(f"Missing Password Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # Test missing name and email for new user
    data = {
        "username": "newuser2@example.com",
        "password": "pass123"
    }
    
    response = requests.post(f"{BASE_URL}/token/", json=data)
    print(f"Missing Name/Email Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("Testing Token API Endpoint")
    print("=" * 50)
    print()
    
    try:
        test_register_new_user()
        test_login_existing_user()
        test_invalid_credentials()
        test_missing_fields()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"Error: {e}") 