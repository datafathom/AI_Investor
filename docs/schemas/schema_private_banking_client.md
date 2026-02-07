# Schema: Private Banking Client

## File Location
`schemas/private_banking_client.py`

## Purpose
Pydantic models for private banking clients and tax deferral strategies, serving ultra-high-net-worth individuals with specialized wealth management features.

---

## Models

### PrivateBankingClientBase
**Private banking client profile.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Client identifier | Attribution |
| `client_tier` | `str` | `"UHNW"` | Tier: `HNW`, `UHNW`, `FAMILY_OFFICE` | Service level |
| `total_relationship_value` | `float` | *required* | Total assets with firm | Relationship sizing |
| `assigned_banker_id` | `Optional[UUID]` | `None` | Private banker | Relationship |
| `service_level` | `str` | `"PLATINUM"` | Level: `GOLD`, `PLATINUM`, `BLACK` | Service tier |
| `direct_indexing_eligible` | `bool` | `True` | Can use direct indexing | Feature access |
| `alternative_investments_eligible` | `bool` | `True` | Can access alternatives | Feature access |

---

### PrivateBankingClient
**Full private banking client record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `created_at` | `datetime` | `datetime.now()` | Onboarding date | Audit |

---

### TaxDeferralStrategyBase
**Tax deferral strategy configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `client_id` | `UUID` | *required* | Client | Attribution |
| `strategy_type` | `str` | *required* | Type: `EXCHANGE_FUND`, `OPPORTUNITY_ZONE`, `INSTALLMENT_SALE` | Strategy |
| `estimated_tax_savings` | `float` | `0.0` | Projected savings | Value proposition |
| `implementation_cost` | `float` | `0.0` | Setup costs | Cost analysis |
| `holding_period_years` | `int` | *required* | Required holding period | Logistics |
| `liquidity_impact` | `str` | *required* | Impact: `MINIMAL`, `MODERATE`, `SIGNIFICANT` | Trade-offs |

---

### TaxDeferralStrategy
**Full tax deferral strategy record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `status` | `str` | `"PROPOSED"` | Status: `PROPOSED`, `APPROVED`, `IMPLEMENTED` | Workflow |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `PrivateBankingService` | UHNW client management |
| `TaxStrategyService` | Tax optimization |
| `AlternativeInvestmentService` | Alts access |
