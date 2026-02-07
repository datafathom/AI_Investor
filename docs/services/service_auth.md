# Backend Service: Auth

## Overview
The **Auth Service** provides a multi-layered security architecture designed for the high-stakes environment of a personal financial OS. It combines biometric non-repudiation via WebAuthn, multi-tenant isolation for privacy, and unique legacy-planning features like the "Dead Man's Switch."

## Core Security Pillars

### 1. Sovereign Auth Gateway (`sovereign_auth_service.py`)
This is the "Sovereign Kernel" of the system.
- **Role**: All "write-level" API actions (trades, transfers, config edits) require a valid cryptographic signature.
- **Mechanism**: Implements a **WebAuthn challenge-response cycle**.
    - **Command Binding**: Every challenge is cryptographically bound to the hash of the specific command payload, ensuring users sign exactly what is executed.
    - **Single-Use**: Challenges are consumed immediately or expire after 120 seconds to prevent replay attacks.
- **Latency**: Performance is optimized for <300ms total loop budget.

### 2. Multi-Tenant Isolation (`tenant_manager.py`)
Ensures strict data privacy between different family offices or sub-entities using the platform.
- **Role**: The "Landlord" component that manages tenant-specific schemas (e.g., `tenant_alpha`).
- **RBAC**: Implements Role-Based Access Control with standard roles: `admin`, `trader`, and `viewer`.

### 3. Inheritance & Dead Man's Switch (`inheritance_service.py`)
A critical feature for long-term wealth preservation and continuity.
- **Role**: Monitors tenant activity heartbeats.
- **Logic**: If no activity is detected for a configurable threshold (default: 30 days), the **Sovereign Inheritance Protocol** is triggered.
- **Action**: Automatically executes asset transfer logic to pre-configured heir wallets or distributes encrypted access keys.

### 4. MFA & Identity Integration
- **MFA Service (`mfa_service.py`)**: standard TOTP (Time-based One-Time Password) support using `pyotp` for secondary verification of critical overrides.
- **Social Connectors**: Provides legacy OAuth2 integrations for **Google**, **Facebook**, and **Reddit** for initial onboarding or low-stakes utility.

## Dependencies
- `pyotp`: Powers the MFA TOTP logic.
- `cryptography`: Provides secure hashing and challenge generation.
- `utils.database_manager`: Used by the Inheritance service to persist heartbeat data in PostgreSQL.

## Usage Examples

### Generating a Sovereign Challenge for a Trade
```python
from services.auth.sovereign_auth_service import sovereign_auth_service

# Define the command intent
trade_payload = {"action": "BUY", "symbol": "BTC", "amount": 0.5}

# Generate challenge bound to this specific move
challenge = sovereign_auth_service.generate_challenge(trade_payload)
print(f"Generated Challenge: {challenge['challenge_id']} (Expires in {challenge['expires_in_seconds']}s)")
```

### Recording a User Heartbeat
```python
from services.auth.inheritance_service import inheritance_service

# Call this on every dashboard load or critical action
inheritance_service.record_heartbeat(tenant_id="family_alpha")
```
