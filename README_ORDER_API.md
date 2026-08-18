# Order Management API Documentation

## Overview
This API provides comprehensive order management functionality for the Kushnath Ayurveda platform, including order creation, status management, delivery tracking, and shipment creation.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### 1. Create Order
**POST** `/orders/`

Creates a new order from cart items with delivery pincode validation.

**Request Body:**
```json
{
    "customer_mobile": "9876543210",
    "cart_id": 1,
    "delivery_address_id": 1,
    "payment_method": "prepaid",
    "recipient_name": "John Doe",
    "recipient_phone": "9876543210",
    "notes": "Please deliver in the morning"
}
```

**Response:**
```json
{
    "id": 1,
    "order_id": "ABC12345",
    "customer": 1,
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_mobile": "9876543210",
    "status": "pending",
    "payment_status": "pending",
    "payment_method": "prepaid",
    "delivery_address": 1,
    "delivery_pincode": "110001",
    "delivery_city": "New Delhi",
    "delivery_state": "Delhi",
    "delivery_country": "India",
    "recipient_name": "John Doe",
    "recipient_phone": "9876543210",
    "subtotal": "1500.00",
    "shipping_cost": "0.00",
    "discount_amount": "0.00",
    "total_amount": "1500.00",
    "is_deliverable": true,
    "shipment_created": false,
    "tracking_number": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "items": [
        {
            "id": 1,
            "product": 1,
            "product_name": "Ayurvedic Medicine",
            "product_image": "http://localhost:8000/media/products/medicine.jpg",
            "quantity": 2,
            "unit_price": "750.00",
            "total_price": "1500.00"
        }
    ],
    "status_history": [
        {
            "id": 1,
            "status": "pending",
            "changed_by": null,
            "changed_by_name": null,
            "changed_at": "2024-01-15T10:30:00Z",
            "notes": "Order created"
        }
    ]
}
```

### 2. Get All Orders
**GET** `/orders/`

Retrieves all orders with filtering and pagination.

**Query Parameters:**
- `status`: Filter by order status (pending, confirmed, processing, shipped, delivered, cancelled, refunded)
- `payment_status`: Filter by payment status (pending, paid, failed, refunded)
- `payment_method`: Filter by payment method (cod, prepaid)
- `customer_mobile`: Filter by customer mobile number
- `start_date`: Filter orders from this date (YYYY-MM-DD)
- `end_date`: Filter orders until this date (YYYY-MM-DD)
- `min_amount`: Filter orders with minimum amount
- `max_amount`: Filter orders with maximum amount
- `search`: Search in order_id, customer name, recipient name, delivery pincode
- `ordering`: Sort by field (-field for descending)

**Example:**
```
GET /orders/?status=pending&customer_mobile=9876543210&ordering=-created_at
```

### 3. Get Order Details
**GET** `/orders/{id}/`

Retrieves detailed information about a specific order.

### 4. Update Order Status
**PATCH** `/orders/{id}/update_status/`

Updates the status of an order.

**Request Body:**
```json
{
    "new_status": "confirmed",
    "notes": "Order confirmed by admin"
}
```

### 5. Create Shipment
**POST** `/orders/{id}/create_shipment/`

Creates a shipment for the order using Delhivery API.

**Response:**
```json
{
    "id": 1,
    "order_id": "ABC12345",
    "status": "shipped",
    "shipment_created": true,
    "tracking_number": "DLV123456789",
    "shipment_details": {
        "packages": [
            {
                "waybill": "DLV123456789",
                "status": "created"
            }
        ]
    }
}
```

### 6. Cancel Order
**POST** `/orders/{id}/cancel_order/`

Cancels an order with optional refund for prepaid orders.

**Request Body:**
```json
{
    "cancellation_reason": "Customer requested cancellation"
}
```

### 7. Refund Order
**POST** `/orders/{id}/refund_order/`

Refunds a prepaid order.

**Request Body:**
```json
{
    "refund_reason": "Product damaged during delivery"
}
```

### 8. Dashboard Statistics
**GET** `/orders/dashboard_stats/`

Retrieves dashboard statistics.

**Response:**
```json
{
    "total_orders": 150,
    "pending_orders": 25,
    "processing_orders": 15,
    "shipped_orders": 30,
    "delivered_orders": 70,
    "cancelled_orders": 10,
    "total_revenue": "150000.00",
    "today_revenue": "5000.00",
    "cod_orders": 80,
    "prepaid_orders": 70
}
```

### 9. Recent Orders
**GET** `/orders/recent_orders/`

Retrieves recent orders for dashboard.

**Query Parameters:**
- `limit`: Number of orders to retrieve (default: 10)

### 10. Orders by Customer
**GET** `/orders/orders_by_customer/`

Retrieves all orders for a specific customer.

**Query Parameters:**
- `customer_mobile`: Customer mobile number (required)

### 11. Order Status History
**GET** `/order-status-history/`

Retrieves order status history.

**Query Parameters:**
- `order_id`: Filter by order ID
- `status`: Filter by status
- `changed_by`: Filter by user who changed status

## Order Status Flow

1. **pending** → Order created, awaiting confirmation
2. **confirmed** → Order confirmed by admin
3. **processing** → Order being processed
4. **shipped** → Shipment created and order shipped
5. **delivered** → Order delivered to customer
6. **cancelled** → Order cancelled
7. **refunded** → Order refunded (for prepaid orders)

## Payment Status Flow

1. **pending** → Payment pending
2. **paid** → Payment received
3. **failed** → Payment failed
4. **refunded** → Payment refunded

## Delivery Integration

### Pincode Validation
The API automatically validates delivery pincodes using the Delhivery API:
- Endpoint: `https://staging-express.delhivery.com/api/dc/fetch/serviceability/pincode/`
- Token: `0368e03c66b1fc26848d7d4bed4798c45de2b3cf`

### Shipment Creation
Shipments are created using the Delhivery API:
- Endpoint: `https://staging-express.delhivery.com/api/cmu/create.json`
- Token: `0368e03c66b1fc26848d7d4bed4798c45de2b3cf`

## Error Responses

### 400 Bad Request
```json
{
    "error": "Delivery not available for this pincode."
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Usage Examples

### Frontend Integration

#### Create Order
```javascript
const createOrder = async (orderData) => {
    const response = await fetch('/api/orders/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(orderData)
    });
    return response.json();
};
```

#### Get Orders by Customer
```javascript
const getCustomerOrders = async (mobileNumber) => {
    const response = await fetch(`/api/orders/orders_by_customer/?customer_mobile=${mobileNumber}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
};
```

#### Update Order Status
```javascript
const updateOrderStatus = async (orderId, newStatus, notes) => {
    const response = await fetch(`/api/orders/${orderId}/update_status/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            new_status: newStatus,
            notes: notes
        })
    });
    return response.json();
};
```

#### Create Shipment
```javascript
const createShipment = async (orderId) => {
    const response = await fetch(`/api/orders/${orderId}/create_shipment/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
};
```

## Admin Dashboard Features

The admin interface provides:
- Complete order management
- Status updates with bulk actions
- Order filtering and search
- Delivery tracking
- Shipment management
- Financial reporting
- Customer order history

## Notes

1. **Pincode Validation**: Orders are only created if the delivery pincode is serviceable by Delhivery.
2. **Cart Clearing**: After order creation, the customer's cart is automatically cleared.
3. **Status History**: All status changes are logged with timestamps and user information.
4. **Refund Handling**: Only prepaid orders can be refunded.
5. **Shipment Creation**: Shipments can only be created for confirmed or processing orders.
6. **Unique Order IDs**: Each order gets a unique 8-character alphanumeric ID. 