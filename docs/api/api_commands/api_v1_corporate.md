# API Service: api_v1_corporate

This document contains all endpoints registered under `api_v1_corporate`.

## GET /api/v1/corporate/earnings

**Summary**: Retrieve historical and upcoming corporate earnings events.

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

