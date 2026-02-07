# Backend Service: Security (The Vault)

## Overview
The **Security Service** is the platform's defensive perimeter, containing **28 specialized modules** for identity management, encryption, and emergency protocols. It protects UHNW clients from both cyber threats and real-world incapacity scenarios.

## Core Components (Selected)

### 1. Dead Man Switch (`dead_man_switch.py`)
Digital Inheritance Protocol.
- **Check-In System**: Requires periodic user verification.
- **Trigger Threshold**: If 30 days pass without check-in, releases crypto keys/shards to designated beneficiaries.

### 2. Encryption Service (`encryption_service.py`)
- AES-256 encryption for data at rest.
- Key rotation and secure key storage.

### 3. KYC Service (`kyc_service.py`)
- Know Your Customer compliance for onboarding.
- Identity verification and sanction screening.

### 4. Supporting Modules
- `shamir_sharing.py`: Splits secret keys into shards.
- `pqc_keygen.py`: Post-Quantum Cryptography key generation.
- `geofence_service.py`: Location-based access restrictions.
- `panic_service.py`: Emergency lockout and asset freeze.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Security Settings** | Dead Man Switch | `dead_man_switch.check_in()` | **Missing** |
| **Vault** | Key Manager | `shamir_sharing`, `encryption_service` | **Partially Implemented** |

## Usage Example

```python
from services.security.dead_man_switch import DeadManSwitchService

switch = DeadManSwitchService()

# User confirms they are alive
switch.check_in()

# Check status
status = switch.verify_status()
print(f"Switch Status: {status['status']}")
print(f"Days Until Trigger: {status.get('days_until_trigger', 'N/A')}")
```
