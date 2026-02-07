# Backend Service: Middleware (Sovereign Kernel)

## Overview
The **Middleware Service** (also known as the **Sovereign Kernel**) operates as the gatekeeper for the entire platform. It enforces the system's "Zero-Trust" security model by intercepting every HTTP request before it reaches business logic. Its most critical component is the **Sovereign Signature Enforcement**, which mandates that all state-mutating operations (writes/edits) must be cryptographically signed by a hardware authenticator (WebAuthn/YubiKey/TouchID), preventing unauthorized changes even if a session token is hijacked. Additionally, it handles high-performance caching (Redis) and rate-limiting to protect external API quotas.

## Core Components

### 1. Sovereign Signature Enforcement (`sovereign_signature_middleware.py`)
the "Nuclear Keys" of the platform.
- **Biometric Write-Protection**: Intercepts `POST`, `PUT`, and `DELETE` requests to critical endpoints (e.g., `v1/ledger`, `v1/orders`). It rejects any request that lacks a valid `X-Sovereign-Signature` header.
- **Challenge-Response Protocol**: Verifies that the signature was generated using a private key held on the user's physical device (Passkey) and matches the specific command payload, preventing replay attacks.
- **Authorization Bypass (Dev Mode)**: Includes a strict "Dev-Only" bypass for local testing, which must be disabled in production.

### 2. API Gateway Cache (`cache_layer.py`)
Reduces latency and external costs.
- **Response Caching**: Caches idempotent `GET` requests (e.g., market data quotes, portfolio summaries) in Redis. This prevents redundant calls to expensive external providers like AlphaVantage or Bloomberg, significantly reducing API costs.
- **Smart Invalidation**: (Planned) Automatically invalidates cache entries when underlying data changes (e.g., a new trade clears).

### 3. Failover & Rate Limiter (`failover.py`, `rate_limiter.py`)
Ensures system resilience.
- **Circuit Breaker**: Detects when a primary data provider (e.g., primary exchange feed) is down and automatically routes requests to a backup provider.
- **Quota Enforcer**: Tracks API usage against defined limits (e.g., "5 calls/min to AlphaVantage"). It queues or rejects excess requests to prevent account bans.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Global** | API Client (`apiClient.js`) | `cache_layer` | **Partially Implemented** (Basic caching headers present) |
| **All Write Forms** | "Sign & Submit" Modal | `sovereign_signature_middleware` | **Missing / Backend Only** |
| **System Monitor** | Gateway Health Status | `rate_limiter` | **Missing / Backend Only** |

> [!WARNING]
> **Frontend Gap Identifier**: The `Sovereign-Signature` header is currently enforced on the backend but is **NOT yet implemented** in the frontend `apiClient.js`. Write operations will currently fail with `401 Unauthorized` until the frontend functionality for WebAuthn signing is built.

## Dependencies
- `fastapi`: Provides the dependency injection framework for attaching middleware to routes.
- `services.auth.sovereign_auth_service`: Performs the actual cryptographic verification of the signatures.
- `redis`: (Implied) Backing store for cache and rate-limit counters.

## Usage Examples

### Protecting a Critical Route with Sovereign Signature
```python
from fastapi import APIRouter, Depends
from services.middleware.sovereign_signature_middleware import require_sovereign_signature

router = APIRouter()

@router.post("/ledger/transfer", dependencies=[Depends(require_sovereign_signature)])
async def execute_transfer(transfer_request: TransferSchema):
    # This code ONLY executes if the request has a valid cryptographic signature
    # matching the transfer_request body.
    return ledger.process_transfer(transfer_request)
```

### Checking Rate Limits before External Call
```python
from services.middleware.rate_limiter import GatewayRateLimiter

limiter = GatewayRateLimiter()

if limiter.is_allowed(provider="OPENAI"):
    # Safe to call API
    response = call_openai_gpt4()
else:
    # Rate limit exceeded
    raise HTTPException(status_code=429, detail="Rate limit exceeded for AI provider")
```
