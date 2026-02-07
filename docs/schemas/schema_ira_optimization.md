# Schema: IRA Optimization

## File Location
`schemas/ira_optimization.py`

## Purpose
Pydantic models for IRA optimization analysis including Traditional vs. Roth contribution strategies based on current and projected tax rates.

---

## Models

### IRAOptimizationProfileBase
**User's tax profile for IRA optimization.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Profile owner | Attribution |
| `current_marginal_rate` | `float` | *required* | Current marginal tax rate | Tax comparison |
| `current_effective_rate` | `Optional[float]` | `None` | Current effective tax rate | Tax analysis |
| `current_agi` | `Optional[float]` | `0.0` | Adjusted Gross Income | Income context |
| `filing_status` | `str` | *required* | Status: `SINGLE`, `MARRIED_JOINT`, `HEAD_OF_HOUSEHOLD` | Tax bracket lookup |
| `projected_retirement_rate` | `Optional[float]` | `None` | Expected retirement tax rate | Future tax |
| `projected_retirement_income` | `Optional[float]` | `0.0` | Expected retirement income | Projection input |
| `expected_social_security` | `Optional[float]` | `0.0` | Expected SS benefits | Income projection |
| `expected_pension_income` | `Optional[float]` | `0.0` | Expected pension | Income projection |
| `current_age` | `int` | *required* | User's current age | Timeline |
| `retirement_age` | `int` | *required* | Target retirement age | Timeline |
| `life_expectancy` | `int` | `90` | Assumed life expectancy | Projection horizon |

---

### IRAOptimizationProfile
**Full optimization profile with recommendations.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `years_to_retirement` | `int` | `0` | Computed years to retirement | Timeline |
| `recommended_strategy` | `Optional[str]` | `None` | Strategy: `TRADITIONAL`, `ROTH`, `SPLIT` | Recommendation |
| `split_percentage_roth` | `Optional[float]` | `0.0` | Recommended Roth percentage | Split strategy |
| `recommendation_confidence` | `Optional[float]` | `0.0` | Confidence score | Reliability |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |
| `updated_at` | `datetime` | `datetime.now()` | Last update | Freshness |

---

### AnalysisResult
**IRA comparison analysis output.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `traditional_value` | `float` | *required* | Projected Traditional IRA value | Comparison |
| `roth_value` | `float` | *required* | Projected Roth IRA value | Comparison |
| `breakeven_rate` | `float` | *required* | Tax rate where both equal | Decision point |
| `recommendation` | `str` | *required* | Strategy recommendation | Guidance |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `IRAOptimizationService` | Strategy analysis |
| `TaxProjectionService` | Tax rate forecasting |
| `RetirementPlanningService` | Retirement integration |

## Related Database
- `schemas/postgres/ira_optimization.sql` - Profile table
