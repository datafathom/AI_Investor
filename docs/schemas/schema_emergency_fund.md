# Schema: Emergency Fund

## File Location
`schemas/emergency_fund.py`

## Purpose
Pydantic models for emergency fund tracking, including liquid cash reserves, coverage calculations, and risk assessments. Helps users maintain adequate emergency savings based on their income stability and expenses.

---

## Models

### EmergencyFundBase
**Base model for emergency fund data.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Fund owner | Attribution |
| `total_liquid_cash` | `float` | *required* | Total liquid assets | Primary metric |
| `checking_balance` | `Optional[float]` | `0.0` | Checking account balance | Component tracking |
| `savings_balance` | `Optional[float]` | `0.0` | Savings account balance | Component tracking |
| `money_market_balance` | `Optional[float]` | `0.0` | Money market balance | Component tracking |
| `monthly_expenses` | `float` | *required* | Average monthly expenses | Coverage calculation |
| `coverage_tier` | `Optional[str]` | `"ADEQUATE"` | Coverage level: `CRITICAL`, `LOW`, `ADEQUATE`, `STRONG` | Risk assessment |
| `income_stability_score` | `Optional[float]` | `50.0` | Income stability (0-100) | Risk factor |
| `career_risk_factor` | `Optional[float]` | `50.0` | Job security risk (0-100) | Risk factor |

---

### EmergencyFund
**Full emergency fund record with computed fields.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `annual_expenses` | `float` | `0.0` | Yearly expense total | Annual planning |
| `months_of_coverage` | `float` | `0.0` | How many months fund covers | Key metric |
| `last_calculated` | `datetime` | `datetime.now()` | Last calculation time | Freshness |
| `created_at` | `datetime` | `datetime.now()` | Record creation | Audit |

---

### EmergencyFundKafkaMessage
**Kafka event message for emergency fund updates.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | User identifier | Routing |
| `liquid_cash` | `float` | *required* | Current liquid cash | Event data |
| `monthly_expenses` | `float` | *required* | Monthly expenses | Event data |
| `months_coverage` | `float` | *required* | Coverage months | Event data |
| `coverage_tier` | `str` | *required* | Coverage tier | Event data |
| `alert_level` | `str` | *required* | Alert severity | Notification triggering |
| `timestamp` | `datetime` | `datetime.now()` | Event time | Event ordering |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `EmergencyFundService` | Fund analysis |
| `LinkedAccountService` | Balance aggregation |
| `AlertService` | Low coverage alerts |
| `Kafka` | Event streaming |
