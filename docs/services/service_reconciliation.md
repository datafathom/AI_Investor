# Backend Service: Reconciliation (The Auditor)

## Overview
The **Reconciliation Service** ensures that the platform's internal records match external sources of truth (brokerages, banks). It detects "drift" caused by missed transactions, API errors, or data corruption.

## Core Components

### 1. Consistency Checker (`consistency_checker.py`)
- **Ledger Verification**: Compares internal balance against broker-reported balance.
- **Drift Detection**: Flags discrepancies greater than $0.01 as reconciliation failures, triggering alerts.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Admin Dashboard** | Reconciliation Status | `consistency_checker.verify_ledger()` | **Implicit** (Runs as background job) |

## Usage Example

```python
from services.reconciliation.consistency_checker import ConsistencyChecker
from decimal import Decimal

checker = ConsistencyChecker()

# Compare internal vs. broker balance
is_ok, drift = checker.verify_ledger(
    internal_balance=Decimal("125000.45"),
    broker_balance=Decimal("125000.43")
)

print(f"Consistent: {is_ok}, Drift: ${drift}")
```
