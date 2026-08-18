# 🛒 Order Management System

## Overview
This system provides comprehensive order management for both Cash on Delivery (COD) and Razorpay online payments. All checkout data is saved to Django models with proper payment status tracking.

## 🗄️ Database Models

### 1. CustomerOrder
Main order information including customer details, delivery address, payment method, and order status.

**Fields:**
- `order_number` - Auto-generated unique order number (e.g., ORD20241201123456)
- `order_date` - Timestamp when order was created
- `order_status` - Order lifecycle status (pending, confirmed, processing, shipped, delivered, cancelled, returned)
- `customer_name`, `customer_email`, `customer_phone` - Customer information
- `delivery_address`, `delivery_city`, `delivery_state`, `delivery_pincode`, `delivery_country` - Delivery details
- `payment_method` - Payment method (cod, razorpay)
- `payment_status` - Payment status (pending, processing, completed, failed, cancelled, refunded)
- `payment_date` - When payment was completed
- `subtotal`, `shipping_cost`, `total_savings`, `final_total` - Amount breakdown
- `razorpay_order_id`, `razorpay_payment_id`, `razorpay_signature` - Razorpay-specific fields
- `notes` - Additional order notes

### 2. OrderItem
Individual items in each order with product details and pricing.

**Fields:**
- `order` - Foreign key to CustomerOrder
- `product_id` - Product ID from frontend
- `product_name`, `product_image` - Product information
- `quantity` - Quantity ordered
- `unit_price` - Price per unit (discounted price)
- `total_price` - Total price for this item
- `discount_price` - Discounted price per unit
- `original_price` - Original product price

### 3. PaymentTransaction
Payment tracking and transaction history.

**Fields:**
- `order` - Foreign key to CustomerOrder
- `transaction_id` - Unique transaction identifier
- `amount`, `currency` - Transaction amount and currency
- `status` - Transaction status (pending, processing, completed, failed, cancelled, refunded)
- `payment_method` - Payment method used
- `gateway_response` - JSON response from payment gateway
- `created_at`, `updated_at` - Timestamps

## 🔌 API Endpoints

### 1. Create Order
```
POST /api/orders/create/
```
Creates a new order for both COD and Razorpay payments.

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+91 98765 43210",
  "delivery_address": "123 Main Street",
  "delivery_city": "Mumbai",
  "delivery_state": "Maharashtra",
  "delivery_pincode": "400001",
  "delivery_country": "India",
  "payment_method": "cod",
  "subtotal": 150.00,
  "shipping_cost": 0.00,
  "total_savings": 20.00,
  "final_total": 130.00,
  "notes": "Test order",
  "items": [
    {
      "id": 1,
      "name": "Test Product",
      "image": "https://example.com/image.jpg",
      "quantity": 2,
      "price": 75.00,
      "discountPrice": 65.00
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Order created successfully",
  "order_id": 1,
  "order_number": "ORD20241201123456",
  "payment_status": "pending",
  "order_status": "confirmed"
}
```

### 2. Get Order Details
```
GET /api/orders/{order_id}/
```
Retrieves complete order information including items and transactions.

### 3. Update Payment Status
```
POST /api/orders/{order_id}/payment-status/
```
Updates payment status and order status based on payment completion.

**Request Body:**
```json
{
  "payment_status": "completed",
  "razorpay_payment_id": "pay_1234567890",
  "razorpay_signature": "signature_hash"
}
```

## 🔄 Payment Flow

### Cash on Delivery (COD)
1. **Order Creation**: Order is created with `payment_status: pending` and `order_status: confirmed`
2. **Payment Status**: Remains `pending` until payment is collected on delivery
3. **Order Status**: Immediately `confirmed` since no online payment is required

### Razorpay Online Payment
1. **Order Creation**: Order is created with `payment_status: pending` and `order_status: pending`
2. **Payment Processing**: Customer is redirected to Razorpay payment page
3. **Payment Completion**: After successful payment, `payment_status` is updated to `completed`
4. **Order Confirmation**: `order_status` is automatically updated to `confirmed`
5. **Success Redirect**: Customer is redirected to success page

## 🚀 Frontend Integration

### Checkout Page Updates
The `AyurvedaCheckoutPage.jsx` has been updated to:
- Create orders using the new Django API
- Handle both COD and Razorpay payment methods
- Pass order data to Razorpay payment page
- Redirect to Django payment page for Razorpay orders

### Key Changes
1. **Order Creation**: All checkout data is sent to `/api/orders/create/`
2. **Payment Method Handling**: Different flows for COD vs Razorpay
3. **Data Passing**: Order information passed via URL parameters to payment page
4. **Status Tracking**: Payment and order status are properly tracked

## 🧪 Testing

### Test Page
Use `api/test_order_system.html` to test:
- COD order creation
- Razorpay order creation
- Payment page functionality
- Order details retrieval

### Test Scenarios
1. **Create COD Order**: Test order creation without payment
2. **Create Razorpay Order**: Test order creation with pending payment
3. **Test Payment Page**: Verify payment page loads correctly
4. **Check Order Details**: Verify order data is saved correctly

## 📋 Database Migrations

After adding the new models, run:
```bash
cd api/
python manage.py makemigrations
python manage.py migrate
```

## 🔧 Configuration

### Django Settings
Ensure templates directory is configured:
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        # ... other settings
    },
]
```

### CORS Settings
Frontend domain should be in CORS allowed origins:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]
```

## 🎯 Benefits

1. **Complete Data Tracking**: All checkout information is saved
2. **Payment Status Management**: Proper tracking of payment completion
3. **Order Lifecycle**: Full order status management
4. **Audit Trail**: Complete transaction history
5. **Scalability**: Structured data for future enhancements
6. **Integration Ready**: Easy to integrate with inventory and shipping systems

## 🚨 Important Notes

1. **Server Restart**: Django server must be restarted after template directory changes
2. **Database Migration**: Run migrations after adding new models
3. **Order Numbers**: Auto-generated unique order numbers
4. **Payment Verification**: Razorpay payments are verified before status update
5. **Error Handling**: Comprehensive error handling for all API endpoints

## 🔍 Troubleshooting

### Common Issues
1. **Template Not Found**: Restart Django server after settings changes
2. **Migration Errors**: Check model syntax and field definitions
3. **API Errors**: Verify endpoint URLs and request data format
4. **Payment Issues**: Check Razorpay configuration and test mode settings

### Debug Tools
- Use `api/test_order_system.html` for testing
- Check Django console for error messages
- Verify database migrations are applied
- Test API endpoints individually



