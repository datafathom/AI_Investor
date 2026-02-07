# Schema: Contribution

## File Location
`schemas/contribution.py`

## Purpose
Pydantic models for tracking retirement account contributions, including employee and employer matches. Monitors contribution limits, year-to-date totals, and remaining contribution room.

---

## Models

### ContributionBase
**Base model for contribution tracking.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Account owner | Linking to user |
| `account_id` | `UUID` | *required* | Retirement account | Account identification |
| `contribution_date` | `date` | *required* | Date of contribution | Timing |
| `employee_contribution` | `float` | *required* | Employee's contribution amount | Tracking employee savings |
| `employer_match` | `float` | *required* | Employer matching contribution | Match calculation |
| `ytd_employee_total` | `Optional[float]` | `0.0` | Year-to-date employee contributions | Limit tracking |
| `ytd_employer_total` | `Optional[float]` | `0.0` | Year-to-date employer contributions | Match tracking |
| `ytd_total` | `Optional[float]` | `0.0` | Combined year-to-date total | Overall contribution tracking |
| `annual_limit` | `Optional[float]` | `0.0` | IRS annual contribution limit | Compliance |
| `remaining_room` | `Optional[float]` | `0.0` | Remaining contribution capacity | Planning |

---

### ContributionCreate
**Create model (inherits from ContributionBase).**

No additional fields - used for API input validation.

---

### Contribution
**Full contribution record with computed fields.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique contribution identifier | Primary key |
| `total_contribution` | `float` | `0.0` | Combined employee + employer total | Summary |
| `created_at` | `datetime` | `datetime.now()` | Record creation time | Audit |

**Config:** `from_attributes = True` - Enables ORM mode.

---

## Integration Points

| Service | Usage |
|---------|-------|
| `ContributionService` | Contribution recording |
| `EmployerMatchService` | Match calculation |
| `RetirementPlanningService` | Contribution optimization |
| `ComplianceService` | Limit monitoring |

## Related Schemas
- `employer_match.py` - Employer match configuration
- `ira_optimization.py` - IRA optimization strategies
