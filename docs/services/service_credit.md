# Backend Service: Credit

## Overview
The **Credit Service** is a dual-purpose financial engine. It manages personal credit health (monitoring, improvement, and simulation) while providing institutional-grade risk analysis for private credit and direct lending portfolios. It ensures that both the user's credit profile and the platform's credit-based investments are optimized for maximum yield and stability.

## Core Components

### 1. Consumer Credit intelligence
- **Credit Monitoring (`credit_monitoring_service.py`)**: 
    - **Score Tracking**: Monitors FICO/VantageScore trends across multiple timeframes.
    - **Factor Analysis**: Deconstructs credit scores into weighted factors (Payment History, Utilization, etc.) to identify specific areas of weakness.
- **Improvement Engine (`credit_improvement_service.py`)**:
    - **Personalized Recommendations**: Generates actionable items (e.g., "Set up autopay," "Request limit increase") with estimated impact scores.
    - **Score Simulator**: Projects future credit scores based on completed action items and projected timeframes.

### 2. Institutional Private Credit
- **Credit Risk Engine (`credit_risk_engine.py`)**: 
    - **Net Yield Calibration**: Calculates the expected net yield for direct lending by adjusting gross spreads for base rates, annual default probabilities, and recovery rates.
    - **Risk Status Classification**: Automatically flags portfolios as `STABLE` or `WATCHLIST` based on expected loss thresholds.
- **Loan Tape Ingestion (`loan_tape_svc.py`)**: Processes raw institutional loan tapes (Principal, Counterparty, Maturity) into unified portfolio committed-capital metrics.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Credit Dashboard** | Score Trend Graph | `credit_monitoring_service.get_credit_history()` |
| **Credit Dashboard** | Impact Simulator | `credit_improvement_service.simulate_score_improvement()` |
| **Credit Dashboard** | Action Center | `credit_improvement_service.generate_recommendations()` |
| **Private Credit Workstation** | Yield Calculator | `credit_risk_engine.calculate_expected_net_yield()` |
| **Private Credit Workstation** | Tape Ingestion Portal | `loan_tape_svc.ingest_tape()` |

## Dependencies
- `decimal`: Used for high-precision financial math in the yield engine.
- `pydantic`: Enforces schemas for `CreditScore`, `CreditRecommendation`, and `CreditProjection`.
- `services.system.cache_service`: Persists recent snapshots of credit scores and projections.

## Usage Examples

### Simulating a Credit Score Improvement
```python
from services.credit.credit_improvement_service import get_credit_improvement_service

improvement_svc = get_credit_improvement_service()

# user_id identifies the specific credit profile
projection = await improvement_svc.simulate_score_improvement(
    user_id="user_vanguard_99",
    recommendations=[rec1, rec2] # recommendation objects from generate_recommendations()
)

print(f"Projected Score: {projection.projected_score} by {projection.projected_date}")
```

### Calculating Expected Net Yield for Private Credit
```python
from services.credit.credit_risk_engine import CreditRiskEngine
from decimal import Decimal

risk_engine = CreditRiskEngine()

stats = risk_engine.calculate_expected_net_yield(
    gross_spread_bps=450,
    base_rate=Decimal("0.0525"),
    default_prob_annual=Decimal("0.015"),
    recovery_rate=Decimal("0.65")
)

print(f"Net Yield: {stats['net_yield_pct']}% (Status: {stats['risk_status']})")
```
