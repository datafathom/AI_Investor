# Schema: Retirement

## File Location
`schemas/retirement.py`

## Purpose
Pydantic models for retirement planning including withdrawal strategies, scenario modeling, and income projections through retirement.

---

## Models

### WithdrawalStrategy
**Retirement withdrawal strategy configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy identifier | Primary key |
| `user_id` | `str` | *required* | Strategy owner | Attribution |
| `strategy_type` | `str` | *required* | Type: `4_percent`, `guardrails`, `bucket`, `dynamic` | Approach |
| `initial_withdrawal_rate` | `float` | *required* | Starting withdrawal rate | Base rate |
| `inflation_adjustment` | `bool` | `True` | Adjust for inflation | Purchasing power |
| `floor_rate` | `Optional[float]` | `None` | Minimum withdrawal rate | Guardrails |
| `ceiling_rate` | `Optional[float]` | `None` | Maximum withdrawal rate | Guardrails |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |

---

### RetirementScenario
**Retirement planning scenario.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `scenario_id` | `str` | *required* | Scenario identifier | Primary key |
| `scenario_name` | `str` | *required* | Display name | Identification |
| `retirement_age` | `int` | *required* | Target retirement age | Timeline |
| `life_expectancy` | `int` | `95` | Planning horizon | Duration |
| `initial_portfolio` | `float` | *required* | Starting value | Baseline |
| `annual_expenses` | `float` | *required* | Expected expenses | Spending |
| `social_security` | `float` | `0.0` | SS benefit | Income |
| `pension` | `float` | `0.0` | Pension benefit | Income |
| `other_income` | `float` | `0.0` | Other income sources | Income |
| `inflation_rate` | `float` | `0.03` | Assumed inflation | Adjustment |
| `expected_return` | `float` | `0.07` | Portfolio return | Growth |

---

### ProjectedIncome
**Projected retirement income by year.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `year` | `int` | *required* | Projection year | Timeline |
| `age` | `int` | *required* | Age in year | Reference |
| `portfolio_value` | `float` | *required* | Portfolio value | Wealth |
| `withdrawal_amount` | `float` | *required* | Annual withdrawal | Income |
| `social_security` | `float` | *required* | SS income | Income |
| `pension` | `float` | *required* | Pension income | Income |
| `total_income` | `float` | *required* | Total income | Summary |
| `expenses` | `float` | *required* | Annual expenses | Spending |
| `surplus_deficit` | `float` | *required* | Income vs expenses | Gap |

---

### RetirementSimulationResult
**Monte Carlo simulation results.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `simulation_id` | `str` | *required* | Simulation identifier | Primary key |
| `scenario_id` | `str` | *required* | Source scenario | Linking |
| `success_rate` | `float` | *required* | Probability of success | Key metric |
| `median_ending_value` | `float` | *required* | Median terminal wealth | Outcome |
| `percentile_5` | `float` | *required* | 5th percentile value | Downside |
| `percentile_95` | `float` | *required* | 95th percentile value | Upside |
| `years_of_data` | `List[ProjectedIncome]` | *required* | Year-by-year projections | Detail |
| `simulation_runs` | `int` | `10000` | Number of simulations | Methodology |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `RetirementPlanningService` | Scenario management |
| `WithdrawalStrategyService` | Strategy configuration |
| `MonteCarloService` | Simulations |

## Frontend Components
- Retirement dashboard (FrontendRetirement)
- Scenario builder
- Income projection charts
- Success probability gauge
