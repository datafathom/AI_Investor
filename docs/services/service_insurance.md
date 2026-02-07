# Backend Service: Insurance

## Overview
The **Insurance Service** manages the platform's specialized risk-wrapper and tax-alpha infrastructure. It is designed for UHNW and institutional clients utilizing **Private Placement Life Insurance (PPLI)**, **Corporate-Owned Life Insurance (COLI)**, and premium financing. The service optimizes asset placement by ranking investments based on their "Tax Drag," monitors the health of policy-backed loans, and proactively flags lapse risks to ensures the long-term structural integrity of the legacy plan.

## Core Components

### 1. PPLI Efficiency & Tax-Drag Ranking (`ppli_efficiency_svc.py`, `efficiency_ranker.py`)
Determines the optimal assets to place inside a tax-exempt insurance wrapper.
- **Tax-Drag Analysis**: Calculates the impact of ordinary income, short-term capital gains, and high turnover on an asset's net performance.
- **Priority Placement**: Automatically ranks a client's portfolio, flagging assets with a high "Efficiency Gap" as "CRITICAL" candidates for PPLI wrapping (e.g., credit-heavy funds or high-turnover hedge strategies).

### 2. Policy Loan & Lapse Tracker (`loan_tracker.py`)
The monitoring layer for insurance-collateralized liquidity.
- **Wash Loan Management**: Logs and verifies "Wash Loans" where borrowing costs are offset by policy credits, enabling tax-free access to capital.
- **Lapse Risk Projection**: Continuously monitors the ratio of loan balance to cash value. It calculates the remaining years of "Cost of Insurance" (COI) coverage, triggering high-severity alerts if a policy is projected to lapse within 5 years.

### 3. Withdrawal & Distribution Modeling (`ppli_withdrawal.py`)
- **Tax-Free Distributions**: Models distributions via the "FIFO" (Basis First) principle and subsequent loans to maintain the policy's tax-favored status under IRS Section 7702.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Insurance Station** | PPLI Wrapper Optimizer | `ppli_efficiency_svc.rank_assets_by_tax_drag()` |
| **Insurance Station** | Lapse Risk Countdown | `ppli_loan_tracker.calculate_lapse_risk()` |
| **Portfolio Detail** | Tax-Drag Impact Card | `efficiency_ranker.rank_assets()` |
| **Document Hub** | Policy Ledger (Loans) | `ppli_loan_tracker.log_loan_transaction()` |
| **Planning Station** | PPLI Withdrawal Preview | `ppli_withdrawal.py` (Withdrawal math) |

## Dependencies
- `decimal`: Used for all high-precision financial math involving tax rates, yields, and loan interest.
- `logging`: Records structural events like "High Lapse Risk" and "PPLI Priority Shifts."

## Usage Examples

### Ranking Assets for a PPLI Shield
```python
from services.insurance.efficiency_ranker import TaxEfficiencyRanker
from decimal import Decimal

ranker = TaxEfficiencyRanker()

# Sample assets: High-yield bond vs Low-yield tech
assets = [
    {"ticker": "HYG", "yield": 0.08, "turnover": 0.40, "type": "BOND"},
    {"ticker": "AAPL", "yield": 0.01, "turnover": 0.05, "type": "EQUITY"}
]

# Assume 37% ordinary income tax rate
ranking = ranker.rank_assets(assets=assets, ord_rate=Decimal('0.37'), st_rate=Decimal('0.37'))

for r in ranking:
    print(f"Asset: {r['ticker']} | Tax Drag: {r['tax_drag_bps']} bps | Priority: {r['ppli_priority']}")
```

### Checking the Lapse Risk of a Policy Loan
```python
from services.insurance.loan_tracker import PPLILoanTracker
from decimal import Decimal

tracker = PPLILoanTracker()

# Scenario: $2M Cash Value, $1.8M Loan, $50k Annual Cost of Insurance
years_rem = tracker.calculate_lapse_risk(
    cash_value=Decimal('2000000'),
    loan_balance=Decimal('1800000'),
    annual_coi=Decimal('50000')
)

print(f"Policy Health: {years_rem} years of coverage remaining.")
if years_rem < 5:
    print("ACTION REQUIRED: Strategy re-funding or loan repayment recommended.")
```
