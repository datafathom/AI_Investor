# Phase 08: RBAC Enforcement
> **Phase ID**: 08
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement Role-Based Access Control (RBAC) to restrict API access based on user roles (e.g., `admin`, `trader`, `analyst`, `auditor`). This layer sits on top of the JWT authentication to ensure granular permissioning.

## Objectives
- [ ] Update `generate_token` to include user roles (mocked).
- [ ] Implement `@requires_role(role)` decorator in `auth_utils.py`.
- [ ] Apply RBAC to sensitive endpoints (e.g., Kill Switch -> `admin`, Secrets -> `admin`).
- [ ] Verify RBAC via unit tests.
- [ ] (Optional) Update Frontend to simulate Role switching.

## Files to Modify
1.  `web/auth_utils.py`: Add `requires_role` decorator.
2.  `web/api/auth_api.py`: Mock roles during login (Admin vs Trader).
3.  `web/api/wave_apis.py`: Protect `kill-switch` and `secrets` endpoints.
4.  `tests/system/test_rbac.py` **[NEW]**: Unit tests for role enforcement.

## Technical Design

### Decorator: `@requires_role`
```python
def requires_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check g.user_role or decode token
            if g.user_role != required_role:
                return 403 Forbidden
            return f(*args, **kwargs)
        return wrapper
    return decorator
```

### Roles Hierarchy (Simple)
- `admin`: Access to everything.
- `trader`: Access to trading, kill switch.
- `analyst`: Read-only access to market data.
- `auditor`: Read-only access to compliance logs.

## Verification
- Unit Test: 
    - Create token with `role='analyst'`.
    - Attempt to access `requires_role('admin')` endpoint -> 403.
    - Create token with `role='admin'` -> 200.
