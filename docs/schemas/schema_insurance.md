# Schema: Insurance

## File Location
`schemas/insurance.py`

## Purpose
Pydantic models for insurance providers and policies. Tracks life insurance, PPLI (Private Placement Life Insurance), and umbrella policies for comprehensive wealth protection planning.

---

## Models

### InsuranceProviderBase
**Insurance company information.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `name` | `str` | *required* | Provider name | Display |
| `provider_type` | `str` | *required* | Provider category | Classification |
| `am_best_rating` | `Optional[str]` | `None` | AM Best financial rating | Credit quality |
| `specializations` | `List[str]` | `[]` | Product specializations | Matching |
| `licensed_states` | `List[str]` | `[]` | Licensed jurisdictions | Availability |

---

### InsuranceProvider
**Full insurance provider record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

### InsurancePolicyBase
**Insurance policy details.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `client_id` | `UUID` | *required* | Policy holder | Ownership |
| `provider_id` | `UUID` | *required* | Insurance company | Provider link |
| `policy_type` | `str` | *required* | Type: `TERM_LIFE`, `WHOLE_LIFE`, `PPLI`, `UMBRELLA` | Classification |
| `policy_number` | `str` | *required* | Policy identifier | Tracking |
| `death_benefit` | `Optional[float]` | `0.0` | Death benefit amount | Coverage |
| `cash_value` | `Optional[float]` | `0.0` | Accumulated cash value | Asset value |
| `annual_premium` | `float` | *required* | Yearly premium | Cost |
| `effective_date` | `date` | *required* | Policy start date | Timing |
| `expiration_date` | `Optional[date]` | `None` | Policy end date | Term tracking |

---

### InsurancePolicy
**Full insurance policy record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `status` | `str` | `"ACTIVE"` | Status: `ACTIVE`, `LAPSED`, `CANCELLED` | Lifecycle |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `InsuranceService` | Policy management |
| `EstatePlanningService` | Life insurance in estate |
| `PPLIService` | PPLI-specific features |

## Related Database
- `schemas/postgres/insurance_providers.sql` - Provider table
