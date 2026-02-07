# Schema: Fee Billing

## File Location
`schemas/fee_billing.py`

## Purpose
Pydantic models for advisor fee schedules and billing records. Supports AUM-based tiered fee structures and billing cycle management for advisory relationships.

---

## Models

### FeeScheduleBase
**Advisor fee schedule configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `client_id` | `UUID` | *required* | Client being billed | Client identification |
| `advisor_id` | `UUID` | *required* | Billing advisor | Advisor attribution |
| `fee_type` | `str` | *required* | Type: `AUM`, `PERFORMANCE` | Fee structure |
| `base_fee_pct` | `Optional[float]` | `0.0` | Base fee percentage | Simple fee calculation |
| `tier_1_max` | `Optional[float]` | `1000000.0` | First tier AUM limit | Tiered pricing |
| `tier_1_rate` | `Optional[float]` | `0.0100` | First tier rate (100 bps) | Tiered pricing |
| `tier_2_max` | `Optional[float]` | `5000000.0` | Second tier AUM limit | Tiered pricing |
| `tier_2_rate` | `Optional[float]` | `0.0075` | Second tier rate (75 bps) | Tiered pricing |
| `tier_3_rate` | `Optional[float]` | `0.0050` | Third tier rate (50 bps) | Tiered pricing |
| `billing_frequency` | `str` | `"QUARTERLY"` | Billing cycle | Schedule |
| `effective_date` | `date` | *required* | When schedule starts | Timing |

---

### FeeSchedule
**Full fee schedule record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

### BillingRecordBase
**Individual billing record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `fee_schedule_id` | `UUID` | *required* | Associated fee schedule | Links to schedule |
| `billing_period_start` | `date` | *required* | Period start date | Timing |
| `billing_period_end` | `date` | *required* | Period end date | Timing |
| `aum_at_billing` | `float` | *required* | AUM used for calculation | Fee basis |
| `gross_fee` | `float` | *required* | Fee before adjustments | Calculation |
| `proration_factor` | `float` | `1.0` | Proration multiplier | Partial period |
| `net_fee` | `float` | *required* | Final billed amount | Invoice amount |

---

### BillingRecord
**Full billing record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `status` | `str` | `"PENDING"` | Status: `PENDING`, `PAID`, `CANCELLED` | Workflow |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `FeeCalculationService` | Fee computation |
| `BillingService` | Invoice generation |
| `InstitutionalService` | Advisory billing |

## Related Database
- `schemas/postgres/fee_billing.sql` - Billing tables
