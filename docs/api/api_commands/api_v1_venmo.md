# API Service: api_v1_venmo

This document contains all endpoints registered under `api_v1_venmo`.

## POST /api/v1/venmo/payment/venmo/pay

**Summary**: Process Venmo payment.

### Details
- **Authentication**: None
- **Rate Limiting**: 100/min
- **Caching**: None

### Response Body
```json
{
  "200": {
    "description": "OK"
  }
}
```

### Error Codes
| Code | Description |
| --- | --- |
| 400 | Bad Request |
| 401 | Unauthorized |
| 500 | Server Error |

---

