# Schema: Public API

## File Location
`schemas/public_api.py`

## Purpose
Pydantic models for public API management including API keys, usage tracking, rate limiting, and tier-based access control.

---

## Enums

### APITier
**API access tiers with different rate limits.**

| Value | Description |
|-------|-------------|
| `FREE` | Limited free access |
| `BASIC` | Basic paid tier |
| `PRO` | Professional tier |
| `ENTERPRISE` | Unlimited enterprise access |

---

## Models

### APIKey
**API key for external access.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `key_id` | `str` | *required* | Unique key ID | Primary key |
| `user_id` | `str` | *required* | Key owner | Attribution |
| `key_hash` | `str` | *required* | Hashed API key | Authentication |
| `name` | `str` | *required* | Key display name | Identification |
| `tier` | `APITier` | `FREE` | Access tier | Rate limiting |
| `rate_limit` | `int` | `100` | Requests per minute | Throttling |
| `is_active` | `bool` | `True` | Whether key is active | Access control |
| `scopes` | `List[str]` | `[]` | Permitted scopes | Authorization |
| `created_date` | `datetime` | *required* | Key creation | Audit |
| `last_used_date` | `Optional[datetime]` | `None` | Last request | Activity |
| `expires_date` | `Optional[datetime]` | `None` | Key expiration | Security |

---

### APIUsage
**API usage tracking record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `usage_id` | `str` | *required* | Unique usage ID | Primary key |
| `key_id` | `str` | *required* | API key used | Linking |
| `endpoint` | `str` | *required* | Endpoint called | Analytics |
| `method` | `str` | *required* | HTTP method | Analytics |
| `status_code` | `int` | *required* | Response status | Monitoring |
| `response_time_ms` | `int` | *required* | Latency in ms | Performance |
| `request_date` | `datetime` | *required* | Request timestamp | Timeline |
| `ip_address` | `Optional[str]` | `None` | Client IP | Security |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `PublicAPIService` | API key management |
| `RateLimitingService` | Throttling |
| `APIAnalyticsService` | Usage analytics |

## Frontend Components
- Developer portal (FrontendAPI)
- API key management
- Usage dashboard
