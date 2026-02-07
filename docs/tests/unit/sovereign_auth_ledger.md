# Documentation: `tests/unit/test_sovereign_auth.py`

## Overview
This test suite validates the "Zero-Trust" identity layer. It ensures that every command executed by the Sovereign OS is properly challenged and signed using WebAuthn-compatible mechanisms.

## Components Under Test
- `services.auth.sovereign_auth_service.SovereignAuthService`: Core identity and challenge issuance.
- `schemas.sovereign_ledger.JournalEntry`: Integrity of the triple-entry accounting system.

## Key Test Scenarios

### 1. Challenge Lifecycle
- **Goal**: Ensure challenges are temporary, unique, and tamper-proof.
- **Assertions**:
    - Challenges expire after a set duration (e.g., 120s).
    - Consumption is limited to "single-use"—reusing a challenge ID raises a failure.
    - Performance: 100 challenges generated in < 50ms (0.5ms per challenge).

### 2. Payload Integrity
- **Goal**: Prevent "Man-in-the-Middle" or "Replay" attacks on commands.
- **Assertions**: If the `command_payload` used during verification differs by even one key from the original, the signature is rejected as "not matching".

### 3. Balanced Ledger Accounting
- **Goal**: Enforce strict double-entry accounting at the schema level.
- **Assertions**:
    - Journal entries must have `debit == credit`.
    - Unbalanced entries raise a `ValueError` during Pydantic validation.

## Holistic Context
This is the "Security Backbone". By enforcing balanced ledger entries and single-use WebAuthn challenges, the system makes it mathematically impossible to "leak" money or execute unauthorized trades without a cryptographic audit trail.
