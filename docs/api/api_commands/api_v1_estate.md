# API Service: api_v1_estate

This document contains all endpoints registered under `api_v1_estate`.

## GET /api/v1/estate/heartbeat

**Summary**: Check the "Dead Man's Switch" status for Estate execution.

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

