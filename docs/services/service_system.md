# Backend Service: System (The Operating Core)

## Overview
The **System Service** contains **24 foundational modules** that power the platform's infrastructure. It manages caching, secrets, health checks, authentication, and cross-cutting concerns that all other services depend on.

## Core Components (Selected)

### 1. Cache Service (`cache_service.py`)
- **Redis Backend**: Uses Redis for high-performance distributed caching.
- **In-Memory Fallback**: Automatically falls back to in-memory cache if Redis is unavailable.
- **TTL Support**: All cached items have configurable time-to-live.

### 2. Secret Manager (`secret_manager.py`)
- Environment variable loading with `.env` support.

### 3. Vault Secret Manager (`vault_secret_manager.py`)
- HashiCorp Vault integration for production secrets.

### 4. Other Key Modules
- `totp_service.py`: Time-based One-Time Password generation for MFA.
- `health_check_service.py`: Liveness and readiness probes.
- `social_auth_service.py`: OAuth2 flows for Google, Discord, etc.
- `tracing_service.py`: Distributed tracing for debugging.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings** | MFA Setup | `totp_service` | **Implemented** |
| **Health Monitor** | Status Page | `health_check_service` | **Implemented** (`HealthToast.jsx`) |

## Usage Example

```python
from services.system.cache_service import get_cache_service

cache = get_cache_service()

# Set a value with 1-hour TTL
cache.set("user:123:preferences", {"theme": "dark"}, ttl=3600)

# Get a value
prefs = cache.get("user:123:preferences")
print(prefs)  # {"theme": "dark"}
```
