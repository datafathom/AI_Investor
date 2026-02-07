# API Service: api_v1_margin

This document contains all endpoints registered under `api_v1_margin`.

## GET /api/v1/margin/status

**Summary**: Check current margin utilization and buffer levels.

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

