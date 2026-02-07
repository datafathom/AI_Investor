# Backend Service: Custody

## Overview
The **Custody Service** is the platform's asset safeguarding and title verification layer. It is designed to ensure that the user's financial assets are held in the safest possible registration formats—primarily shifting from "Street Name" brokered positions to **Direct Registration (DRS)** with transfer agents. Additionally, it maintains the primary **Immutable Ledger**, providing cryptographic proof of every transaction on the platform.

## Core Components

### 1. DRS Transfer Manager (`drs_transfer_mgr.py`)
Automates the legal transition of asset ownership.
- **Direct Registration (DRS)**: Provides an automated workflow for moving shares from a broker (Source) to a Transfer Agent (Destination). This places the legal title of the security directly in the client's name.
- **Title Verification**: Includes logic for verifying the registration status of any asset (e.g., `DRS`, `PHYSICAL`, `ISSUER_DIRECT`) to determine the level of direct ownership.

### 2. Immutable Ledger Service (`ledger_service.py`)
Provides the "Truth Machine" for platform activity.
- **Cryptographic Chaining**: Uses SHA-256 hashing to chain every transaction to the previous entry, ensuring that any modification to historical data is detectable.
- **Integrity Validation**: Periodically audits the entire chain of ledger entries to ensure there have been no modifications or corruption.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Portfolio Terminal** | Registration Status Ribbon | `drs_transfer_manager.verify_legal_title()` |
| **Asset Detail Page** | DRS Transfer Wizard | `drs_transfer_manager.initiate_drs_transfer()` |
| **Vault / Audit Center** | Transaction History Ledger | `ledger_service.verify_chain_integrity()` |
| **Trust Workstation** | Title Evidence Locker | `drs_transfer_manager.verify_legal_title()` |

## Dependencies
- `hashlib`: Standard Python library for ledger checksumming and transaction chaining.
- `schemas.platform_ledger`: Defines the data structure for consistent ledger serialization.

## Usage Examples

### Initiating a DRS Transfer for Asset Protection
```python
from services.custody.drs_transfer_mgr import DRSTransferManager
from uuid import uuid4

drs_mgr = DRSTransferManager()

# Transfer 100 shares of an asset (UUID) to the Transfer Agent
ticket = drs_mgr.initiate_drs_transfer(
    asset_id=uuid4(),
    broker_id=uuid4(),
    share_quantity=100
)

print(f"DRS Transfer Ticket {ticket['transfer_ticket_id']} has status {ticket['status']}")
```

### Verifying Ledger Integrity
```python
from services.custody.ledger_service import LedgerService

ledger = LedgerService()

# entries: List[PlatformLedger] fetched from DB
is_valid = ledger.verify_chain_integrity(entries)

if not is_valid:
    print("CRITICAL ALERT: Ledger chain integrity failure detected!")
```
