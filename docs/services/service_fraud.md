# Backend Service: Fraud

## Overview
The **Fraud Service** serves as the platform's independent security and integrity auditor. Its primary mission is to detect reporting anomalies and structural fraud patterns (e.g., Ponzi schemes) that might otherwise be obscured by traditional performance metrics. By enforcing strict data-provenance rules and analyzing return volatility, it protects clients from third-party advisor malpractice.

## Core Components

### 1. Anti-Madoff Guard (`anti_madoff_guard.py`)
A specialized detection engine for reporting-based fraud.
- **Statement Source Validation**: Implements a "Zero-Trust" policy for financial data. It mandates that any statement or valuation data must originate directly from a **Qualified Custodian**, flagging any data provided solely by an investment advisor as a high-risk security violation.
- **Return Striation Detection**: Uses statistical analysis (standard deviation) to identify suspiciously "smooth" return profiles. If a manager reports consistent positive monthly returns with a volatility threshold below 0.1% (Standard Deviation < 0.001) over a 12-month period, the service triggers a `MADOFF_PATTERN` alert.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Institutional Audit** | Fraud Alert Table | `anti_madoff_guard.detect_return_striation()` |
| **Custodian Hub** | Data Provenance Shield | `anti_madoff_guard.validate_statement_source()` |
| **Manager Detail** | Volatility Consistency Meter | `anti_madoff_guard.detect_return_striation()` |
| **Compliance Station** | System Security Pulse | All Fraud alerts |

## Dependencies
- `numpy`: Used for high-precision statistical standard deviation calculations over return series.

## Usage Examples

### Detecting Suspiciously Consistent Returns
```python
from services.fraud.anti_madoff_guard import AntiMadoffGuard

guard = AntiMadoffGuard()

# 12 months of "too good to be true" 1% monthly returns
fake_returns = [0.0101, 0.0099, 0.0102, 0.01, 0.0098, 0.0101, 0.0102, 0.01, 0.0099, 0.0101, 0.01, 0.0102]

is_fraudulent = guard.detect_return_striation(returns=fake_returns)

if is_fraudulent:
    print("CRITICAL ALERT: Potential Ponzi pattern detected (Low Volatility Striation)")
```

### Validating Statement Provenance
```python
from services.fraud.anti_madoff_guard import AntiMadoffGuard

guard = AntiMadoffGuard()

# Scenario: Advisor uploads a PDF they authored themselves
is_valid = guard.validate_statement_source(
    provider_name="Jones Wealth Advisor LLC",
    custodian_name="Fidelity Institutional"
)

if not is_valid:
    print("ACTION BLOCKED: Data must originate from a verified custodian source.")
```
