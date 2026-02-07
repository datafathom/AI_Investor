# Backend Service: Alerts

## Overview
The **Alerts Service** provides a diverse range of monitoring and notification capabilities designed to flag critical risks and high-conviction signals. It covers multiple domains including geopolitical exposure, demographic shifts in macroeconomic data, personal liquidity thresholds, and anomalies in institutional trading prints.

## Monitoring Components

### Financial & Market Alerts

#### High Conviction Insider Alert (`high_conviction.py`)
- **Purpose**: Filters market data for significant insider activity.
- **Threshold**: Only flags purchases greater than or equal to **$500,000**.
- **Usage**: Surfaces high-fidelity signals that suggest strong management confidence in a company's future.

#### Factor Decay Monitor (`factor_decay.py`)
- **Purpose**: Detects if historically successful investment factors (e.g., Value, Momentum) are experiencing structural breaks.
- **Logic**: Alerts when the rolling 10-year return of a factor turns negative, suggesting the premium may have disappeared or "decayed."

#### Signature Print Alert (`signature_print.py`)
- **Purpose**: Detects out-of-sequence trade prints ("Z" or "T" codes) which often signal significant institutional intent or late-reporting of large blocks.

---

### Risk Exposure Alerts

#### Conflict Zone Detector (`conflict_zone.py`)
- **Purpose**: Identifies exposure to global geopolitical hotzones in a company's supply chain.
- **Example**: Flags "CRITICAL" risk for tickers like TSM if tensions escalate in the Taiwan Strait.

#### Demographic Risk Monitor (`demographic_risk.py`)
- **Purpose**: Tracks the "Ticking Time Bomb" of 401k net outflows.
- **Logic**: Alerts when Boomer withdrawals exceed Gen Z contributions at a national or fund level, signaling a potential structural headwind for passive index flows.
- **Recommendation**: Suggests hedging passive exposure when flows turn negative.

---

### Personal Liquidity Alerts

#### Emergency Fund Alert Service (`emergency_fund_alerts.py`)
- **Purpose**: A tiered monitoring system for personal cash reserves.
- **Tiers**:
    - **CRITICAL (0-3 months)**: Blocks trades and sends urgent SMS/Email alerts.
    - **LOW (3-6 months)**: Warning status.
    - **ADEQUATE (6-12 months)**: Normal operations.
    - **STRONG/FORTRESS (12+ months)**: High liquidity security.

## Dependencies
- `logging`: Used for `ALERT_LOG` and `ALERT_EVAL` audit trails.
- `datetime`: Used for time-stamped status calculations.

## Usage Example

### Evaluating Emergency Coverage
```python
from services.alerts.emergency_fund_alerts import EmergencyFundAlertService

service = EmergencyFundAlertService()
eval = service.evaluate_coverage(months=2.5)

if eval['action_required']:
    print(f"TRADING LOCKED: {eval['message']}")
```

### Checking Geopolitical Risk
```python
from services.alerts.conflict_zone import ConflictDetector

detector = ConflictDetector()
risk = detector.check_exposure("TSM", ["TAIWAN_STRAIT"])
print(f"Risk Level: {risk['risk']}")
```
