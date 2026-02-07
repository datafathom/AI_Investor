# Schema: Institutional

## File Location
`schemas/institutional.py`

## Purpose
Pydantic models for institutional features including multi-client management, client analytics, white-label configuration, and professional reporting for RIAs and advisory firms.

---

## Models

### Client
**Client record for institutional advisors.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `client_id` | `str` | *required* | Unique client identifier | Primary key |
| `advisor_id` | `str` | *required* | Managing advisor | Relationship |
| `client_name` | `str` | *required* | Client name | Display |
| `portfolio_ids` | `List[str]` | `[]` | Associated portfolios | Portfolio linking |
| `aum` | `float` | `0.0` | Client AUM | Revenue tracking |
| `risk_level` | `str` | `"Low"` | Risk profile: `Low`, `Moderate`, `High` | Risk management |
| `retention_score` | `float` | `100.0` | Client retention probability | Churn prediction |
| `kyc_status` | `str` | `"Verified"` | KYC status: `Verified`, `Pending`, `Flagged` | Compliance |
| `jurisdiction` | `str` | `"US"` | Legal jurisdiction | Compliance |
| `funding_source` | `Optional[str]` | `None` | Source of funds | AML compliance |
| `strategy` | `str` | `"Aggressive AI"` | Investment strategy | Portfolio management |
| `created_date` | `datetime` | *required* | Client onboarding date | Timeline |
| `updated_date` | `datetime` | *required* | Last modification | Tracking |

---

### ClientAnalytics
**Analytics for a specific client.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `client_id` | `str` | *required* | Client identifier | Linking |
| `fee_forecast` | `float` | *required* | Projected fee revenue | Revenue planning |
| `churn_probability` | `float` | *required* | Client churn risk | Retention focus |
| `kyc_risk_score` | `float` | *required* | Compliance risk score | Risk monitoring |
| `rebalance_drift` | `float` | *required* | Portfolio drift from target | Rebalancing trigger |
| `last_updated` | `datetime` | *required* | Analytics refresh time | Freshness |

---

### WhiteLabelConfig
**White-label branding configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `config_id` | `str` | *required* | Configuration identifier | Primary key |
| `organization_id` | `str` | *required* | Organization | Ownership |
| `logo_url` | `Optional[str]` | `None` | Logo image URL | Branding |
| `primary_color` | `Optional[str]` | `None` | Primary brand color | Theming |
| `secondary_color` | `Optional[str]` | `None` | Secondary brand color | Theming |
| `custom_domain` | `Optional[str]` | `None` | Custom domain | White-label URL |
| `branding_name` | `Optional[str]` | `None` | Display name | Branding |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Tracking |

---

### ProfessionalReport
**Professional report for client delivery.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `report_id` | `str` | *required* | Report identifier | Primary key |
| `advisor_id` | `str` | *required* | Generating advisor | Attribution |
| `client_id` | `str` | *required* | Target client | Delivery |
| `report_type` | `str` | *required* | Report category | Classification |
| `content` | `Dict` | `{}` | Report content | Report body |
| `generated_date` | `datetime` | *required* | Generation timestamp | Timing |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `InstitutionalService` | Multi-client management |
| `ProfessionalToolsService` | Professional tools |
| `WhiteLabelService` | Branding configuration |
| `ReportingService` | Client reports |

## Frontend Components
- Institutional dashboard (FrontendInstitutional)
- Client grid view
- White-label settings
- Report generation
