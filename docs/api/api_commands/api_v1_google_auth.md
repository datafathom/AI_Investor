# API Service: api_v1_google_auth

This document contains all endpoints registered under `api_v1_google_auth`.

## GET /api/v1/google_auth/callback

**Summary**: Handle Google OAuth callback.

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

## POST /api/v1/google_auth/callback

**Summary**: Handle Google OAuth callback.

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

## GET /api/v1/google_auth/login

**Summary**: Initiate Google OAuth login flow.

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

## GET /api/v1/google_auth/profile

**Summary**: Get current user's Google profile.

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

## POST /api/v1/google_auth/refresh

**Summary**: Refresh expired access token.

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

## POST /api/v1/google_auth/revoke

**Summary**: Revoke Google access/refresh token.

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

