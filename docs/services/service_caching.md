# Backend Service: Caching

## Overview
The **Caching Service** is the platform's high-performance data persistence layer for transient system states. It is designed to optimize expensive quantitative computations, such as risk simulations and portfolio attribution, by storing results in a low-latency **Redis** backend with a robust in-memory fallback.

## Core Components

### 1. Performance Cache (`performance_cache.py`)
A singleton implementation that provides a tiered caching strategy.

#### Tiers of Storage
1. **Primary (Redis)**: Uses an external Redis instance (configured via `REDIS_URL`) for shared state across distributed service instances.
2. **Fallback (In-Memory)**: Automatically switches to a local Python dictionary if Redis is unavailable, ensuring the system remains functional even during infrastructure degradation.

#### Key Features
- **TTL (Time-To-Live)**: All cached entries support a mandatory expiration window (default: 3600s) to prevent data staleness.
- **Atomic Cache Operations**: Provides high-level methods like `get_or_set` for thread-safe computation and storage patterns.
- **Pattern Invalidation**: Allows clearing specific subsets of cached data using glob-style patterns (e.g., `invalidate_pattern("attribution:*")`).

### 2. The `@cached` Decorator
Enables seamless integration with any internal function. It automatically generates a unique cache key based on the function name and its arguments (using MD5 hashing for complex objects), dramatically reducing the boilerplate required for performance optimization.

## Dependencies
- `redis`: The primary backend driver.
- `hashlib`: Used for deterministic cache key generation.
- `json`: Handles serialization and deserialization of cached Python objects.

## Usage Examples

### Using the `@cached` Decorator
```python
from services.caching.performance_cache import cached

@cached(ttl=300)
def compute_complex_risk_metric(portfolio_id: str, factor: float):
    # This expensive operation will only run once every 5 minutes
    # Results for identical (portfolio_id, factor) pairs will be served from cache
    return some_heavy_math(portfolio_id, factor)
```

### Manual Cache Management
```python
from services.caching.performance_cache import get_cache

cache = get_cache()

# Try to get data with a fallback computation
data = cache.get_or_set(
    key="market_regime:2026-02-07",
    func=determine_market_regime,
    ttl=3600
)

# Invalidate a specific group of keys
cache.invalidate_pattern("auth:challenges:*")
```
