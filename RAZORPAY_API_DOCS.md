# Razorpay API Integration

This document describes the Razorpay payment integration for the Kushnath Ayurveda API.

## Configuration

The Razorpay integration is configured with the following test credentials:
- **Key ID**: `rzp_test_Q79E2maKMiRH3M`
- **Key Secret**: `kP0dd2BxoCc0CjxDrsBO0hMn`

## API Endpoints

### 1. Create Order ID

**Endpoint**: `POST /api/dashboard/rz/orderid/`

**Description**: Creates a new Razorpay order and returns the order ID for payment processing.

**Request Body**:
```json
{
    "amount": 500.00,
    "currency": "INR",
    "receipt": "order_receipt_123"
}
```

**Parameters**:
- `amount` (required): Amount in rupees (will be converted to paise automatically)
- `currency` (optional): Currency code (default: "INR")
- `receipt` (optional): Receipt ID for the order

**Response**:
```json
{
    "success": true,
    "order_id": "order_ABC123XYZ",
    "amount": 50000,
    "currency": "INR",
    "receipt": "order_receipt_123",
    "status": "created",
    "key_id": "rzp_test_Q79E2maKMiRH3M"
}
```

### 2. Get Order Details

**Endpoint**: `GET /api/dashboard/rz/orderid/{order_id}/`

**Description**: Retrieves details of a specific Razorpay order.

**Response**:
```json
{
    "id": 1,
    "order_id": "order_ABC123XYZ",
    "amount": "500.00",
    "currency": "INR",
    "receipt": "order_receipt_123",
    "status": "created",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}
```

## Usage Examples

### Frontend Integration

```javascript
// Create order
const createOrder = async (amount) => {
    try {
        const response = await fetch('/api/dashboard/rz/orderid/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: amount,
                currency: 'INR',
                receipt: `order_${Date.now()}`
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Initialize Razorpay payment
            const options = {
                key: data.key_id,
                amount: data.amount,
                currency: data.currency,
                order_id: data.order_id,
                handler: function (response) {
                    // Handle successful payment
                    console.log('Payment successful:', response);
                },
                prefill: {
                    name: 'Customer Name',
                    email: 'customer@example.com',
                    contact: '9999999999'
                },
                theme: {
                    color: '#3399cc'
                }
            };
            
            const rzp = new Razorpay(options);
            rzp.open();
        }
    } catch (error) {
        console.error('Error creating order:', error);
    }
};
```

### cURL Examples

**Create Order**:
```bash
curl -X POST http://localhost:8000/api/dashboard/rz/orderid/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500.00,
    "currency": "INR",
    "receipt": "order_123"
  }'
```

**Get Order Details**:
```bash
curl -X GET http://localhost:8000/api/dashboard/rz/orderid/order_ABC123XYZ/
```

## Database Model

The `RazorpayOrder` model stores order information:

```python
class RazorpayOrder(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    receipt = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid request data
- `404 Not Found`: Order not found
- `500 Internal Server Error`: Server error

## Security Notes

1. The current implementation uses test credentials
2. For production, move credentials to environment variables
3. Implement proper authentication and authorization
4. Add webhook handling for payment status updates
5. Implement proper error logging and monitoring

## Next Steps

1. Add webhook endpoint for payment status updates
2. Implement payment verification
3. Add order status tracking
4. Integrate with existing order management system
5. Add payment analytics and reporting 