# API Service: api_v1_twilio

This document contains all endpoints registered under `api_v1_twilio`.

## POST /api/v1/twilio/notifications/twilio/send

**Summary**: Send a test SMS alert.

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

