# Razorpay Environment Setup Guide

This guide explains how to configure Razorpay for different environments in the Django backend.

## Environment Configuration

### Development Environment

For local development, the system uses test Razorpay credentials:

**File**: `kushnath_dashboard/settings.py`
```python
# Razorpay Configuration
# Development/Test credentials
RAZORPAY_KEY_ID = 'rzp_test_Q79E2maKMiRH3M'
RAZORPAY_KEY_SECRET = 'kP0dd2BxoCc0CjxDrsBO0hMn'
RAZORPAY_MODE = 'test'  # Set to 'live' for production
```

### Production Environment

For production deployment, the system uses live Razorpay credentials:

**File**: `kushnath_dashboard/settings_production.py`
```python
# Razorpay Configuration for Production
# Live credentials
RAZORPAY_KEY_ID = 'rzp_live_RFVSx4eax0xMjW'
RAZORPAY_KEY_SECRET = 'aMrwajwB1bKan4upU3ukXT24'
RAZORPAY_MODE = 'live'  # Live mode for production
```

## How It Works

1. **Settings Import**: The `dashboard/views.py` imports Razorpay configuration from Django settings:
   ```python
   from django.conf import settings
   
   RAZORPAY_KEY_ID = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_Q79E2maKMiRH3M')
   RAZORPAY_KEY_SECRET = getattr(settings, 'RAZORPAY_KEY_SECRET', 'kP0dd2BxoCc0CjxDrsBO0hMn')
   RAZORPAY_MODE = getattr(settings, 'RAZORPAY_MODE', 'test')
   ```

2. **Automatic Switching**: The system automatically uses the correct credentials based on which settings file is loaded.

3. **Fallback Values**: If settings are not found, the system falls back to test credentials for safety.

## Deployment Instructions

### For Development
- Use the default `settings.py` file
- Test credentials are automatically used
- No additional configuration needed

### For Production
- Use `settings_production.py` file
- Live credentials are automatically used
- Ensure the production settings file is properly configured

## Security Notes

- **Never commit live credentials to version control**
- **Use environment variables for production deployments**
- **Test credentials are safe to use in development**
- **Live credentials should only be used in production environment**

## Testing

### Test Environment
- Use Razorpay test cards for payment testing
- All transactions are simulated
- No real money is processed

### Live Environment
- Real payments are processed
- Use only in production
- Ensure proper SSL/HTTPS configuration

## API Endpoints

The following endpoints automatically use the correct Razorpay configuration:

- `POST /api/dashboard/rz/orderid/` - Create Razorpay order
- `GET /api/dashboard/rz/config/` - Get Razorpay configuration
- `GET /api/dashboard/rz/orderid/{order_id}/` - Get order details

## Frontend Integration

The frontend automatically receives the correct Razorpay key ID from the backend API, ensuring consistency between environments.
