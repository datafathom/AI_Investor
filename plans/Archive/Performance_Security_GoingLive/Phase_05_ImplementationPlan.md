# Phase 05: Secrets Management & Environment Isolation
> **Phase ID**: 05
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement a centralized `SecretManager` service to abstract credential access. This prepares the application for a future HashiCorp Vault integration while enforcing best practices (no hardcoded secrets) in the current environment. We will also introduce a `.env.template` to standardize environment variables.

## Objectives
- [ ] Create `services/system/secret_manager.py` (Singleton).
- [ ] Create `.env.template` base on current usage.
- [ ] Update `SystemHealthDashboard` to display "Vault/Secrets Status".
- [ ] Verify secret retrieval and masking via unit tests.

## Files to Modify/Create
1.  `services/system/secret_manager.py` **[NEW]**
2.  `.env.template` **[NEW]**
3.  `frontend2/src/pages/SystemHealthDashboard.jsx` (Add status indicator)
4.  `web/api/system_api.py` (Add/Update endpoint for vault status)

## Technical Design

### SecretManager
- **Interface**: `get_secret(key, default)`, `get_db_credentials()`.
- **Implementation**: Wraps `os.environ` / `python-dotenv` for now.
- **Security**: Logs access to secrets (masked).

### Frontend
- Update `SystemHealthDashboard.jsx` (which likely uses `KafkaHealth` or similar widgets) to include a "Secrets Engine" status line, simulating a connection to Vault.

## Verification Plan

### Automated Tests
- Create `tests/system/test_secret_manager.py`:
  - Test retrieval of dummy env var.
  - Test masking logic (e.g., `get_masked_secret`).

### Manual Verification
1.  Navigate to `/architect/system`.
2.  Verify "Secrets Engine" shows as "Active (Env)" or "Active (Vault)".
