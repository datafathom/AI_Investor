# Backend Service: Public API ( The Open Door)

## Overview
The **Public API Service** enables the Sovereign OS to be extensible. It allows external developers (or secondary autonomous agents) to interact with the platform programmatically. It handles the "Business of APIs"—issuing keys, enforcing rate limits, and tracking billable usage—so the core services can focus on logic, not infrastructure.

## Core Components

### 1. Public API Service (`public_api_service.py`)
The Gateway.
- **Key Management**: Issues cryptographically secure API keys (`sk_...`) tied to specific users and usage tiers.
- **Rate Limiting**: Enforces quotas based on tiers:
    - **Free**: 100 req/day
    - **Pro**: 1,000 req/day
    - **Enterprise**: 10,000+ req/day
- **Usage Tracking**: Logs every request (endpoint, latency, status) for billing and analytics.

### 2. Developer Portal Service (`developer_portal_service.py`)
The Librarian.
- **Documentation**: Generates OpenAPI specs for the exposed endpoints.
- **SDK Generation**: (Mocked) Provides ready-to-use client libraries for Python and JavaScript to lower the barrier to entry.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Developer Settings** | Key Vault | `public_api_service.create_api_key()` | **Implemented** (`KeyVault.jsx`) |
| **API Dashboard** | Usage Graph | `public_api_service.get_api_usage()` | **Implemented** (`ApiUsage.jsx`) |
| **Marketplace** | Docs Viewer | `developer_portal_service.get_api_documentation()` | **Implemented** (`APIMarketplace.jsx`) |

## Dependencies
- `secrets`: Cryptographically strong random number generation for API keys.
- `schemas.public_api`: Pydantic models for request/response validation.

## Usage Examples

### issuing a New API Key
```python
from services.public_api.public_api_service import get_public_api_service

gateway = get_public_api_service()

# Grant "Pro" access to a user
new_key = await gateway.create_api_key(
    user_id="dev_user_99",
    tier="pro"
)

print(f"Secret Key: {new_key.api_key}")
print(f"Rate Limit: {new_key.rate_limit} req/day")
```

### Tracking a Request
```python
# Middleware calls this largely transparently
await gateway.track_usage(
    api_key_id="key_123",
    endpoint="/api/v1/portfolio",
    response_time_ms=45.2,
    status_code=200
)
```
