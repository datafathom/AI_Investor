# Phase 06: Advanced Authentication
> **Phase ID**: 06
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement Multi-Factor Authentication (MFA) using Time-based One-Time Passwords (TOTP). This enhances security by requiring a second verification step for critical actions (e.g., login, kill switch activation). We will also simulate Hardware Token (YubiKey) support in the UI.

## Objectives
- [ ] Add `pyotp` to `requirements.txt`.
- [ ] Implement `TOTPService` (backend) for generating/verifying codes.
- [ ] Create `MFAVerificationModal` (frontend) for user code input.
- [ ] Protect the `kill-switch` endpoint with MFA enforcement.
- [ ] Update `SystemHealthDashboard` with "Hardware Token" status.

## Files to Modify/Create
1.  `requirements.txt` (Add `pyotp`)
2.  `services/system/totp_service.py` **[NEW]** (Backend MFA logic)
3.  `web/api/auth_api.py` (Add MFA setup/verify endpoints)
4.  `frontend2/src/components/MFAVerificationModal.jsx` **[NEW]**
5.  `frontend2/src/pages/SystemHealthDashboard.jsx` (Add YubiKey status)

## Technical Design

### Backend (`TOTPService`)
- Uses `pyotp` library.
- `generate_secret(user_id)`: Returns base32 secret.
- `verify_code(secret, code)`: Boolean validation.
- Mock YubiKey support: Accept specific hardcoded codes (e.g., "999999") as "hardware" token.

### Frontend (`MFAVerificationModal`)
- Simple Modal with 6-digit input.
- Calls `/api/auth/verify-mfa`.
- On success, executes the protected action.

## Verification Plan

### Automated Tests
- `tests/system/test_totp_service.py`:
  - Test secret generation.
  - Test valid/invalid code verification.

### Browser Verification
1.  Navigate to `/architect/system`.
2.  Verify "Hardware Token" shows "Not Detected" (or similar status).
3.  (Optional) Trigger Kill Switch (Mobile Page) -> Verify Modal appears.
