# Schema: Advisor

## File Location
`schemas/advisor.py`

## Purpose
Defines Pydantic models for financial advisor profiles. This schema captures all necessary information about financial advisors including their registration status, fiduciary obligations, and fee structures. Used throughout the application for advisor onboarding, compliance verification, and client-advisor matching.

---

## Models

### AdvisorBase
**Base model for advisor information. Used for inheritance by create and read models.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `name` | `str` | *required* | Full legal name of the advisor | Displayed in advisor profiles, used for compliance filings and client communications |
| `email` | `EmailStr` | *required* | Primary email address (validated format) | Used for authentication, notifications, and regulatory correspondence |
| `fiduciary_status` | `bool` | `False` | Whether the advisor operates under fiduciary duty | Critical for compliance - fiduciaries must act in client's best interest; affects fee structure options |
| `fiduciary_type` | `Optional[str]` | `None` | Type of fiduciary: `RIA` (Registered Investment Advisor), `BROKER_DEALER`, or `HYBRID` | Determines regulatory requirements, permissible activities, and compliance obligations |
| `registration_type` | `str` | *required* | Registration level: `SEC` (federal) or `STATE` | SEC registration required for AUM > $110M; affects examination authority and reporting |
| `registration_number` | `Optional[str]` | `None` | Official registration identifier | Used for regulatory lookups and ADV form cross-referencing |
| `registration_state` | `Optional[str]` | `None` | Primary state of registration | Required for state-registered advisors; determines applicable state securities laws |
| `sec_crd_number` | `Optional[str]` | `None` | Central Registration Depository number | Unique FINRA identifier for compliance verification and BrokerCheck lookups |
| `firm_name` | `Optional[str]` | `None` | Name of the advisory firm | Used for conflict-of-interest disclosures and firm-level analytics |
| `firm_type` | `Optional[str]` | `None` | Firm structure: `RIA`, `WIREHOUSE`, or `INDEPENDENT` | Affects custody rules, supervisory requirements, and product availability |
| `aum_under_management` | `Optional[float]` | `0.0` | Assets Under Management in dollars | Used for fee tiering, capacity planning, and regulatory threshold monitoring |
| `fee_structure` | `Optional[str]` | `None` | Compensation model: `FEE_ONLY`, `COMMISSION`, or `HYBRID` | Determines conflict-of-interest disclosures and ADV Part 2A requirements |

---

### AdvisorCreate
**Create/input model (inherits all fields from AdvisorBase).**

Used when registering new advisors in the system. No additional fields - serves as a type marker for API input validation.

---

### Advisor
**Full advisor model with system-generated fields.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key for database, used in all advisor-related API calls |
| `created_at` | `datetime` | `datetime.now()` | Account creation timestamp | Audit trail, regulatory record-keeping |
| `updated_at` | `datetime` | `datetime.now()` | Last modification timestamp | Change tracking, cache invalidation |

**Config:** `from_attributes = True` - Enables ORM mode for SQLAlchemy integration.

---

## Integration Points

| Service | Usage |
|---------|-------|
| `AdvisorService` | CRUD operations for advisor management |
| `ComplianceService` | Fiduciary status verification, registration validation |
| `ClientMatchingService` | Matching clients to advisors based on fee structure and fiduciary status |
| `InstitutionalService` | Multi-client management for advisor practices |
| `FeeCalculationService` | Fee calculation based on AUM and fee_structure |

## API Endpoints
- `POST /api/advisors` - Create new advisor (uses `AdvisorCreate`)
- `GET /api/advisors/{id}` - Retrieve advisor profile (returns `Advisor`)
- `PUT /api/advisors/{id}` - Update advisor details
- `GET /api/advisors/search` - Search advisors by registration, firm type, etc.

## Database Table
Maps to `advisors` table in PostgreSQL (see `schemas/postgres/advisors.sql`).

## Frontend Components
- Advisor registration wizard
- Advisor profile dashboard
- Client-advisor matching interface
