# API Service: api_v1_mobile

This document contains all endpoints registered under `api_v1_mobile`.

## POST /api/v1/mobile/kill-switch

**Summary**: Activate system-wide kill switch from a mobile device.

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

