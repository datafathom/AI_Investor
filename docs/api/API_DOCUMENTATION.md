# API Documentation Guide

This guide explains how to use and access the AI Investor API documentation.

## Accessing Documentation

### Swagger UI
Interactive API documentation with "Try it out" functionality:
```
http://localhost:5050/api/docs/swagger-ui
```

### ReDoc
Beautiful, responsive API documentation:
```
http://localhost:5050/api/docs/redoc
```

### OpenAPI Specification
Raw OpenAPI/JSON specification:
```
http://localhost:5050/api/docs/openapi.json
```

## API Overview

### Base URL
- **Production**: `https://api.aiinvestor.com`
- **Development**: `http://localhost:5050`

### Authentication
Most endpoints require authentication via JWT Bearer token:
```http
Authorization: Bearer <your_jwt_token>
```

### Response Format
All API responses follow a consistent format:

**Success Response:**
```json
{
  "success": true,
  "data": {
    // Response data
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "code": 400
}
```

## API Endpoints

### System

#### Health Check
```http
GET /api/v1/health
```

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-21T12:00:00Z"
}
```

### Trading

#### Place Order
```http
POST /api/v1/trading/order
```

Place a trading order.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "side": "BUY",
  "quantity": 10,
  "order_type": "MARKET",
  "time_in_force": "DAY"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": "order_123",
    "status": "FILLED",
    "filled_price": 150.25
  }
}
```

### Portfolio

#### Get Portfolio
```http
GET /api/v1/portfolio
```

Get user's portfolio.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_value": 100000.00,
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 10,
        "avg_price": 150.00,
        "current_price": 150.25,
        "unrealized_pnl": 2.50
      }
    ]
  }
}
```

### Analytics

#### Get Performance Attribution
```http
GET /api/v1/analytics/attribution/{portfolio_id}
```

Get performance attribution analysis.

**Query Parameters:**
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "total_return": 15.5,
    "attribution_by_sector": {
      "Technology": 8.2,
      "Healthcare": 4.3
    }
  }
}
```

## Code Examples

### Python

```python
import requests

BASE_URL = "http://localhost:5050/api/v1"
TOKEN = "your_jwt_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Get portfolio
response = requests.get(f"{BASE_URL}/portfolio", headers=headers)
portfolio = response.json()

# Place order
order_data = {
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 10,
    "order_type": "MARKET"
}
response = requests.post(
    f"{BASE_URL}/trading/order",
    headers=headers,
    json=order_data
)
order = response.json()
```

### JavaScript

```javascript
const BASE_URL = 'http://localhost:5050/api/v1';
const TOKEN = 'your_jwt_token';

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};

// Get portfolio
fetch(`${BASE_URL}/portfolio`, { headers })
  .then(res => res.json())
  .then(portfolio => console.log(portfolio));

// Place order
fetch(`${BASE_URL}/trading/order`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    symbol: 'AAPL',
    side: 'BUY',
    quantity: 10,
    order_type: 'MARKET'
  })
})
  .then(res => res.json())
  .then(order => console.log(order));
```

### cURL

```bash
# Get portfolio
curl -X GET "http://localhost:5050/api/v1/portfolio" \
  -H "Authorization: Bearer your_jwt_token"

# Place order
curl -X POST "http://localhost:5050/api/v1/trading/order" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 10,
    "order_type": "MARKET"
  }'
```

## Error Handling

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "success": false,
  "error": "Error message",
  "code": 400,
  "details": {
    "field": "Additional error details"
  }
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse:
- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per user

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642680000
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

## Webhooks

Subscribe to real-time events via webhooks:

```http
POST /api/v1/webhooks/subscribe
```

**Request Body:**
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["order.filled", "portfolio.updated"]
}
```

## SDKs

Official SDKs are available:
- **Python**: `pip install ai-investor-sdk`
- **JavaScript**: `npm install @ai-investor/sdk`
- **Go**: `go get github.com/ai-investor/go-sdk`

## Support

For API support:
- **Email**: api@aiinvestor.com
- **Documentation**: https://docs.aiinvestor.com
- **Status Page**: https://status.aiinvestor.com

## Changelog

### Version 1.0.0 (2026-01-21)
- Initial API release
- Trading endpoints
- Portfolio management
- Analytics endpoints
