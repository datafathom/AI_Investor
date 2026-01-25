# Phase 17: Redis Caching Layer (Going Live)
> **Phase ID**: 17
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement a high-performance Redis caching layer to reduce database load, accelerate API response times, and handle high-concurrency real-time data feeds. This is a critical step for scaling the platform for public use.

## Objectives
- [ ] Add `redis` to `requirements.txt`.
- [ ] Implement `CacheService` (backend) as a singleton wrapper for Redis.
- [ ] Configure TTL (Time-To-Live) policies for different data types (e.g., 1s for market data, 1h for user settings).
- [ ] Implement Redis-backed session management for the Flask API.
- [ ] Decorate key API endpoints with caching logic:
    - `GET /api/v1/settlement/rates`
    - `GET /api/v1/brokerage/account`
- [ ] Add performance benchmarks to verify speed improvements.

## Files to Modify/Create
1.  `requirements.txt` (Add `redis`)
2.  `services/system/cache_service.py` **[NEW]**
3.  `config/redis_config.json` **[NEW]**
4.  `web/app.py` (Initialize CacheService and session config)
5.  `web/api/settlement_api.py` (Apply caching)

## Technical Design

### Backend (`CacheService`)
- Uses `redis-py`.
- **Simulation Mode**: Fallback to in-memory `dict` if Redis server is unavailable.
- **Namespacing**: Use prefixes (e.g., `ai_investor:rates:`, `ai_investor:session:`) to prevent key collisions.

### API Caching Pattern
- **Cache-Aside**: Check Redis first; if miss, fetch from source and store in Redis.
- **Invalidation**: Implement manual invalidation for data that changes based on user action (e.g., balance updates).

## Verification Plan

### Automated Tests
- `tests/system/test_cache_service.py`:
    - Test set/get/delete operations.
    - Verify TTL expiration.
    - Test fallback to in-memory mode.

### Manual Verification
1.  Enable Redis container.
2.  Measure response time of `/api/v1/settlement/rates` (Initial vs Cached).
3.  Expect latency to drop from ~100ms (Fetch) to <5ms (Redis).
