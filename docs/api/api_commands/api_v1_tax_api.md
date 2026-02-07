# API Service: api_v1_tax_api

This document contains all endpoints registered under `api_v1_tax_api`.

## GET /api/v1/tax_api/tax/harvesting/opportunities

**Summary**: Get tax loss harvesting opportunities.

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

