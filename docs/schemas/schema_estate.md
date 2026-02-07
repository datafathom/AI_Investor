# Schema: Estate

## File Location
`schemas/estate.py`

## Purpose
Pydantic models for estate planning including beneficiary management, estate plans, inheritance projections, and tax optimization scenarios. Supports wealth transfer planning and estate tax minimization strategies.

---

## Enums

### BeneficiaryType
**Beneficiary relationship types.**

| Value | Description |
|-------|-------------|
| `SPOUSE` | Marital partner |
| `CHILD` | Son or daughter |
| `PARENT` | Mother or father |
| `SIBLING` | Brother or sister |
| `OTHER` | Other individual |
| `TRUST` | Trust entity |
| `CHARITY` | Charitable organization |

---

## Models

### Beneficiary
**Estate beneficiary definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `beneficiary_id` | `str` | *required* | Unique beneficiary ID | Primary key |
| `user_id` | `str` | *required* | Estate owner | Attribution |
| `name` | `str` | *required* | Beneficiary name | Display |
| `relationship` | `BeneficiaryType` | *required* | Relationship to owner | Tax treatment |
| `allocation_percentage` | `float` | *required, 0-100* | Inheritance percentage | Distribution |
| `allocation_amount` | `Optional[float]` | `None` | Fixed dollar amount | Alternative allocation |
| `tax_implications` | `Optional[Dict]` | `None` | Tax impact data | Planning |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### EstatePlan
**Complete estate plan.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `plan_id` | `str` | *required* | Unique plan ID | Primary key |
| `user_id` | `str` | *required* | Estate owner | Attribution |
| `total_estate_value` | `float` | *required* | Current estate value | Tax calculations |
| `beneficiaries` | `List[Beneficiary]` | *required* | All beneficiaries | Distribution planning |
| `trust_accounts` | `List[Dict]` | `[]` | Trust structures | Trust planning |
| `tax_exempt_amount` | `float` | `12000000.0` | Federal exemption (2024) | Tax calculations |
| `estimated_estate_tax` | `float` | `0.0` | Projected estate tax | Tax planning |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### InheritanceProjection
**Projected inheritance for a beneficiary.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `projection_id` | `str` | *required* | Unique projection ID | Tracking |
| `beneficiary_id` | `str` | *required* | Target beneficiary | Attribution |
| `projected_inheritance` | `float` | *required* | Gross inheritance | Planning |
| `projected_tax_liability` | `float` | *required* | Expected taxes | Tax planning |
| `after_tax_inheritance` | `float` | *required* | Net inheritance | Final amount |
| `projected_date` | `datetime` | *required* | Projection date | Timeline |
| `assumptions` | `Dict` | *required* | Projection assumptions | Transparency |

---

### EstateScenario
**What-if scenario for estate planning.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `scenario_name` | `str` | *required* | Scenario label | Identification |
| `estate_value` | `float` | *required* | Assumed estate value | Scenario input |
| `beneficiaries` | `List[Dict]` | *required* | Beneficiary allocation | Scenario input |
| `tax_strategies` | `List[str]` | `[]` | Strategies: `gifting`, `trust`, `charitable` | Optimization |
| `projection_years` | `int` | `10` | Projection horizon | Timeline |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `EstatePlanningService` | Plan management |
| `InheritanceSimulator` | Projections |
| `TaxOptimizationService` | Strategy evaluation |

## Frontend Components
- Estate dashboard (FrontendEstate)
- Beneficiary management
- Scenario comparison tool
