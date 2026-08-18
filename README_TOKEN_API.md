# Token API Documentation

## Overview

The token API endpoint at `http://127.0.0.1:8000/api/token/` provides a unified interface for both user authentication (login) and user registration. It automatically detects whether a user exists and handles the appropriate action.

## Endpoint

- **URL**: `POST /api/token/`
- **Content-Type**: `application/json`

## Functionality

### For Existing Users (Login)
If a user with the provided username already exists, the endpoint will:
1. Authenticate the user with the provided credentials
2. Return JWT access and refresh tokens
3. Return user information

### For New Users (Registration)
If a user with the provided username doesn't exist, the endpoint will:
1. Create a new user account
2. Create a customer profile
3. Return JWT access and refresh tokens
4. Return user information

## Request Format

### For Login (Existing Users)
```json
{
    "username": "user@example.com",
    "password": "password123"
}
```

### For Registration (New Users)
```json
{
    "username": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "email": "user@example.com"
}
```

## Response Format

### Successful Login
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "user@example.com",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "message": "Login successful"
}
```

### Successful Registration
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "user@example.com",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "message": "User registered successfully"
}
```

### Error Responses

#### Missing Required Fields (400)
```json
{
    "error": "Username and password are required"
}
```

#### Invalid Credentials (401)
```json
{
    "error": "Invalid credentials"
}
```

#### Missing Registration Fields (400)
```json
{
    "error": "Name and email are required for new user registration"
}
```

#### Invalid Email Format (400)
```json
{
    "error": "Invalid email format"
}
```

#### Email Already Exists (400)
```json
{
    "error": "Email is already registered"
}
```

## Usage Examples

### Using cURL

#### Login
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "password123"
  }'
```

#### Registration
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser@example.com",
    "password": "password123",
    "name": "New User",
    "email": "newuser@example.com"
  }'
```

### Using JavaScript/Fetch

```javascript
// Login or Register
const response = await fetch('http://127.0.0.1:8000/api/token/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'user@example.com',
        password: 'password123',
        name: 'John Doe',  // Required for new users
        email: 'user@example.com'  // Required for new users
    })
});

const data = await response.json();
console.log(data);
```

## Token Usage

After receiving the tokens, you can use them for authenticated requests:

```javascript
// Use access token for API calls
const response = await fetch('http://127.0.0.1:8000/api/protected-endpoint/', {
    headers: {
        'Authorization': `Bearer ${data.access}`
    }
});
```

## Refresh Token

To refresh an expired access token, use the refresh endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token_here"
  }'
```

## Testing

You can test the API using the provided test script:

```bash
python test_token_api.py
```

This will run various test scenarios including:
- User registration
- User login
- Invalid credentials
- Missing required fields

## Notes

- The API automatically creates a Customer profile when registering new users
- Email validation is performed for new registrations
- Username and email must be unique
- Passwords are automatically hashed using Django's built-in password hashing
- JWT tokens have configurable expiration times (5 days for access, 7 days for refresh) 