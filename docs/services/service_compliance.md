# Backend Service: Compliance

## Overview
The **Compliance Service** (internally known as "The Compliance Shield") is the platform's multi-layered regulatory and ethical governance engine. It operates across 49 specialized components to ensure every trade, transfer, and agent action adheres to SEC, FINRA, and fiduciary standards.

## Core Functional Pillars

### 1. The Compliance Engine (`compliance_engine.py`)
The central orchestrator for real-time violation detection.
- **Rule Verification**: Checks transactions against a dynamic library of SEC and FINRA rules.
- **Severity Scoring**: Categorizes violations into `LOW`, `MEDIUM`, or `HIGH` severity for prioritized response.
- **Persistence**: Logs all detected anomalies to the `AuditService` and `RecordVault` for permanent audit trails.

### 2. Market Integrity & Restrictions
- **Wash-Sale Detector (`compliance_service.py`, `wash_sale.py`)**: Analyzes the last 30 days of trading history to prevent the purchase of securities previously sold at a loss, ensuring compliance with IRS tax rules.
- **Insider Trading & Rule 144 (`insider_trading_svc.py`)**: 
    - **Volume Limits**: Calculates 1% of outstanding shares vs. 4-week average weekly volume for affiliate selling.
    - **Lock-Up Validator**: Monitors post-IPO or meta-acquisition lock-up windows.
    - **Compliant Selling Plans**: Validates Rule 10b5-1 selling plans.

### 3. Fiduciary & Trust Governance
- **Solvency Validator (`solvency_validator.py`)**: Ensures asset transfers into Asset Protection Trusts (APTs) are not fraudulent conveyances by performing Balance Sheet and Cash Flow tests.
- **HEMS Validator (`hems_validator.py`)**: Verifies that trust distributions match the legal "Health, Education, Maintenance, and Support" standard.
- **Spendthrift Firewall (`spendthrift_firewall.py`)**: Protects trust assets from external creditor claims by enforcing distribution caps.

### 4. Forensic & Evidence Layer
- **Record Vault (`record_vault.py`)**: A WORM (Write Once, Read Many) style storage system for all compliance-sensitive metadata.
- **Evidence Locker (`evidence_locker.py`)**: Secures snapshots of market states at the time of trade execution for later regulatory defense.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Compliance Dashboard** | Violation Feed | `compliance_engine.get_violations()` |
| **Trade Terminal** | Pre-Flight Modal | `compliance_service.check_wash_sale()` |
| **Strategist / Estate** | APT Solvency Tool | `solvency_validator.generate_solvency_affidavit()` |
| **Insider Workstation** | Role 144 Calculator | `insider_trading_svc.calculate_sellable_volume()` |
| **Audit Center** | Forensic Viewer | `record_vault.get_records_by_type()` |

## Dependencies
- `pydantic`: For robust schema validation of rules and violations.
- `utils.database_manager`: Direct PostgreSQL access for persisting legal affidavits.
- `services.system.cache_service`: For rapid rule-matching and transient state monitoring.

## Usage Examples

### Running a Pre-Trade Wash-Sale Check
```python
from services.compliance.compliance_service import get_compliance_service
from datetime import datetime

compliance = get_compliance_service()

check = compliance.check_wash_sale(ticker="TSLA", trade_date=datetime.now())
if check["is_wash_sale"]:
    print(f"Compliance Block: {check['reason']}")
```

### Validating Insider Sale Volume
```python
from services.compliance.insider_trading_svc import InsiderTradingService

insider_svc = InsiderTradingService()

compliance_report = insider_svc.validate_sale_compliance(
    ticker="NVDA",
    shares_to_sell=50000,
    outstanding_shares=1000000000,
    avg_weekly_volume=30000,
    lockup_expiry=datetime.date(2025, 12, 31)
)

if not compliance_report["compliant"]:
    print(f"SEC RULE 144 FAILURE: {compliance_report['reason']}")
```
