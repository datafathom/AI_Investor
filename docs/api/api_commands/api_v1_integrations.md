# API Service: api_v1_integrations

This document contains all endpoints registered under `api_v1_integrations`.

## GET /api/v1/integrations/connectors

**Summary**: List status of all external API connectors and broker bridges.

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

