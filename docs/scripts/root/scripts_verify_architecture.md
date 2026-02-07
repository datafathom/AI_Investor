# Script: verify_architecture.py

## Overview
`verify_architecture.py` is a specialized Selenium script used to validate the core front-end architectural requirements, specifically the `RequestGuard` and state hydration.

## Core Functionality
- **RequestGuard Testing**: Injects a script into the browser console that attempts to perform a direct `fetch` to an external domain (e.g., Google). It verifies that the application's `RequestGuard` interceptor successfully blocks the request and logs a `GUARD_ACTIVE` message.
- **Cache Persistence**: Checks LocalStorage for specific keys (e.g., `api_cache_`, `last_brokerage_summary`) to ensure that the persistent caching layer is correctly hydrating and storing API responses across sessions.

## Status
**Essential (Security/Architecture)**: Validates critical security constraints (blocking unmanaged external requests) and performance features (offline caching).
