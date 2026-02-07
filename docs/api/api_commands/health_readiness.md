# API Service: health_readiness

This document contains all endpoints registered under `health_readiness`.

## GET /health/readiness

**Summary**: Readiness check - verifies service can accept traffic.

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

