# Schema: Plan 529

## File Location
`schemas/plan_529.py`

## Purpose
Pydantic models for 529 college savings plans including plan details, age-based glide paths, and contribution tracking.

---

## Models

### Plan529Base
**529 plan configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `plan_name` | `str` | *required* | Plan name | Display |
| `state` | `str` | *required* | Plan state | Tax benefits |
| `beneficiary_name` | `str` | *required* | Student name | Attribution |
| `beneficiary_dob` | `date` | *required* | Student birthdate | Age calculation |
| `owner_id` | `UUID` | *required* | Account owner | Ownership |
| `balance` | `float` | `0.0` | Current balance | Value |
| `contribution_ytd` | `float` | `0.0` | YTD contributions | Limit tracking |
| `annual_contribution_limit` | `float` | `18000.0` | Annual gift limit | Compliance |
| `target_enrollment_year` | `int` | *required* | Expected college start | Planning |
| `use_age_based_glide` | `bool` | `True` | Use age-based allocation | Strategy |

---

### Plan529
**Full 529 plan record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `years_until_enrollment` | `int` | `0` | Years to college | Planning |
| `current_allocation` | `Optional[Dict]` | `None` | Current asset allocation | Holdings |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

### GlidePath529
**Age-based allocation glide path.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `years_to_enrollment` | `int` | *required* | Years until college | Phase |
| `equity_allocation` | `float` | *required* | Stock allocation | Asset mix |
| `fixed_income_allocation` | `float` | *required* | Bond allocation | Asset mix |
| `cash_allocation` | `float` | *required* | Cash allocation | Asset mix |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `Plan529Service` | Plan management |
| `GlidePathService` | Allocation guidance |
| `ContributionService` | Contribution tracking |
