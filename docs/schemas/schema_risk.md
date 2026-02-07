# Schema: Risk

## File Location
`schemas/risk.py`

## Purpose
Pydantic models for risk management including VaR calculations, stress testing, risk limits, and portfolio risk profiles.

---

## Models

### VaRResult
**Value at Risk calculation result.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `portfolio_id` | `str` | *required* | Portfolio identifier | Linking |
| `confidence_level` | `float` | *required* | Confidence (0.95, 0.99) | Risk threshold |
| `time_horizon` | `str` | *required* | Horizon: `1d`, `1w`, `1m` | Time period |
| `var_value` | `float` | *required* | VaR dollar amount | Risk metric |
| `var_percentage` | `float` | *required* | VaR as portfolio percentage | Risk metric |
| `method` | `str` | *required* | Method: `historical`, `parametric`, `monte_carlo` | Methodology |
| `calculation_date` | `datetime` | *required* | Calculation timestamp | Freshness |

---

### StressTestScenario
**Stress test scenario definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `scenario_id` | `str` | *required* | Scenario identifier | Primary key |
| `scenario_name` | `str` | *required* | Display name | Identification |
| `scenario_type` | `str` | *required* | Type: `historical`, `hypothetical` | Classification |
| `market_shocks` | `Dict[str, float]` | *required* | Asset class shocks | Scenario definition |
| `description` | `str` | *required* | Scenario description | Context |

---

### StressTestResult
**Stress test result.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `result_id` | `str` | *required* | Result identifier | Primary key |
| `portfolio_id` | `str` | *required* | Tested portfolio | Linking |
| `scenario_id` | `str` | *required* | Applied scenario | Linking |
| `portfolio_loss` | `float` | *required* | Dollar loss | Impact |
| `portfolio_loss_pct` | `float` | *required* | Percentage loss | Impact |
| `holding_impacts` | `List[Dict]` | *required* | Per-holding impacts | Detail |
| `test_date` | `datetime` | *required* | Test timestamp | Timing |

---

### RiskLimit
**Risk limit configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `limit_id` | `str` | *required* | Limit identifier | Primary key |
| `limit_type` | `str` | *required* | Type: `var`, `concentration`, `drawdown` | Category |
| `limit_value` | `float` | *required* | Limit threshold | Threshold |
| `current_value` | `float` | *required* | Current exposure | Monitoring |
| `breach_status` | `str` | *required* | Status: `within`, `warning`, `breach` | Alert |
| `utilization` | `float` | *required* | Limit utilization (0-1) | Headroom |

---

### RiskProfile
**Portfolio risk summary.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `portfolio_id` | `str` | *required* | Portfolio identifier | Linking |
| `volatility` | `float` | *required* | Portfolio volatility | Risk metric |
| `beta` | `float` | *required* | Market beta | Systematic risk |
| `sharpe_ratio` | `float` | *required* | Risk-adjusted return | Quality |
| `max_drawdown` | `float` | *required* | Maximum drawdown | Tail risk |
| `var_95` | `VaRResult` | *required* | 95% VaR | Risk metric |
| `risk_score` | `int` | *required, 1-10* | Composite risk score | Summary |
| `profile_date` | `datetime` | *required* | Profile timestamp | Freshness |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `RiskManagementService` | Risk calculations |
| `StressTestingService` | Scenario testing |
| `RiskMonitoringService` | Limit monitoring |

## Frontend Components
- Risk dashboard (FrontendRisk)
- VaR visualization
- Stress test results
- Risk limit gauges
