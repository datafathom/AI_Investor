# Backend Service: Banking

## Overview
The **Banking Service** serves as the bridge between the Sovereign OS and traditional financial institutions. It enables secure capital onboarding, real-time balance monitoring, and automated cash management workflows such as reconciliation and liquidity sweeps.

## Core Components

### 1. Plaid Integration (`plaid_service.py`, `banking_service.py`)
The primary gateway for connecting to legacy bank accounts.
- **Plaid Service**:
    - **Account Linking**: Generates Link Tokens and exchanges Public Tokens for persistent Access Tokens.
    - **Balance Verification**: Provides real-time "current" and "available" balance checks with a built-in **Rate Limiter** (e.g., 3 checks per hour per user).
    - **Overdraft Protection**: Proactively checks for sufficient funds before triggering funding events.
- **Banking Service Wrapper**: Provides a "Simulation Mode" for developers, allowing the platform to function without active Plaid credentials by using mock data.

### 2. Reconciliation Engine (`reconciliation_service.py`)
Ensures internal accounting matches external truth.
- **Role**: Automatically matches bank transactions with internal system ledger entries.
- **Fuzzy Matching Logic**: Uses a multi-factor matching algorithm:
    - **Amount**: Exact numerical match.
    - **Date**: Matches within a configurable window (e.g., +/- 2 days).
    - **Description**: Uses string similarity (starts-with/contains) to associate bank descriptions (e.g., "Starbucks Coffee") with ledger notes (e.g., "Starbucks NYC").

### 3. Treasury & Cash Flow Management (`treasury_service.py`)
Automates the optimization of liquid capital.
- **Automated Cash Sweeps**: Implements the **"Financial Fortress" threshold logic**. If a checking account balance exceeds a pre-set limit (e.g., $5,000), the excess is automatically "swept" into a higher-yield savings account or emergency fund.
- **Bill OCR Processing**: Features a specialized parser for extracting "Amount Due" and "Due Date" from bill/invoice text, preparing them for automated payment workflows.

## Dependencies
- `plaid-python`: The official SDK for bank connectivity.
- `pyotp`: Used for MFA during sensitive banking operations.
- `pydantic`: Defines structured data models for transactions and accounts.

## Usage Examples

### Initializing a Plaid Link
```python
from services.banking.banking_service import get_banking_service

banking = get_banking_service()
link_token = banking.create_link_token(user_id="user_vanguard_1")

# Frontend will use this token to open the Plaid UI
print(f"Plaid Link Token: {link_token}")
```

### Executing an Automated Cash Sweep
```python
from services.banking.treasury_service import get_treasury_service

treasury = get_treasury_service()
treasury.sync_accounts()

# Sweep any excess above $5000 from primary checking
sweeps = treasury.execute_cash_sweep(threshold=5000.0)

for s in sweeps:
    print(f"Swept ${s['amount']} from {s['source']} to {s['destination']}")
```
