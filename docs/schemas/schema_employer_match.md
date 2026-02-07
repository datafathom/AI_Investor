# Schema: Employer Match

## File Location
`schemas/employer_match.py`

## Purpose
Pydantic models for employer 401(k) match configurations including match types, percentages, caps, and vesting schedules. Enables optimization of employee contributions to maximize employer matching contributions.

---

## Models

### EmployerMatchConfigBase
**Employer match configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Employee | Attribution |
| `employer_name` | `str` | *required* | Company name | Display |
| `match_type` | `str` | `"DOLLAR_FOR_DOLLAR"` | Type: `DOLLAR_FOR_DOLLAR`, `PARTIAL`, `TIERED` | Match calculation |
| `match_percentage` | `float` | *required* | Base match rate | Primary calculation |
| `max_match_percentage` | `Optional[float]` | `None` | Maximum employee contribution matched | Limit enforcement |
| `annual_match_cap` | `Optional[float]` | `None` | Dollar cap on annual match | Limit enforcement |
| `tier_1_employee_pct` | `Optional[float]` | `None` | First tier employee threshold | Tiered match |
| `tier_1_employer_pct` | `Optional[float]` | `None` | First tier employer match rate | Tiered match |
| `tier_2_employee_pct` | `Optional[float]` | `None` | Second tier employee threshold | Tiered match |
| `tier_2_employer_pct` | `Optional[float]` | `None` | Second tier employer match rate | Tiered match |
| `vesting_type` | `Optional[str]` | `"IMMEDIATE"` | Type: `IMMEDIATE`, `CLIFF`, `GRADED` | Vesting calculation |
| `vesting_cliff_months` | `Optional[int]` | `0` | Months until cliff vesting | Cliff vesting |
| `vesting_schedule` | `Optional[Dict[str, float]]` | `None` | Graded schedule: `{"12": 0.20, ...}` | Vesting lookup |
| `effective_date` | `Optional[date]` | `None` | When match policy starts | Policy timing |

---

### EmployerMatchConfig
**Full employer match configuration record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `is_active` | `bool` | `True` | Whether config is current | Active filtering |
| `created_at` | `datetime` | `datetime.now()` | Record creation | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `EmployerMatchService` | Match calculations |
| `ContributionOptimizationService` | Contribution recommendations |
| `VestingService` | Vesting calculations |

## Related Database
- `schemas/postgres/employer_match.sql` - Match configuration table
