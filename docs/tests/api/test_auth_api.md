# Documentation: `tests/api/test_auth_api.py`

## Overview
This test suite covers the security gateway of the application. It validates authentication mechanisms, including traditional credentials, Multi-Factor Authentication (MFA), and social identity providers.

## API Endpoints Under Test
- `POST /api/v1/auth/login`: Credential-based authentication.
- `POST /api/v1/auth/mfa/setup`: TOTP secret generation.
- `POST /api/v1/auth/mfa/verify`: TOTP code verification.
- `GET /api/v1/auth/social/login/{provider}`: OAuth2 initiation.

## Fixtures
- `mock_social_auth_service`: Mocks database-backed user identity retrieval.
- `api_app`: Configures FastAPI with necessary dependency overrides for isolated testing.

## Test Scenarios

### 1. `test_login_success`
- **Goal**: Verify standard JWT issuance for valid users.
- **Assertions**: Returns 200 OK with a valid `token` and user profile.

### 2. `test_mfa_setup_verify_success`
- **Goal**: Validate the TOTP (Time-based One-Time Password) lifecycle.
- **Assertions**:
    - `setup`: Returns a secret and provisioning URI (for QR codes).
    - `verify`: Returns `valid: true` when provided with a correct code.

### 3. `test_social_login_initiate`
- **Goal**: Verify redirection to social providers (e.g., Google).
- **Assertions**: Returns the correct provider `redirect_url`.

## Holistic Context
Auth is the first line of defense. These tests ensure that users can securely enter the system and that high-security features like MFA are mathematically sound and properly exposed.
