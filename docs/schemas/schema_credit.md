# Schema: Credit

## File Location
`schemas/credit.py`

## Purpose
Pydantic models for credit score monitoring, credit factor analysis, improvement recommendations, and credit score projections. Helps users understand and improve their creditworthiness.

---

## Enums

### CreditFactor
**Factors affecting credit scores.**

| Value | Description |
|-------|-------------|
| `PAYMENT_HISTORY` | On-time payment track record (35% of FICO) |
| `CREDIT_UTILIZATION` | Percentage of available credit used (30%) |
| `LENGTH_OF_HISTORY` | Age of credit accounts (15%) |
| `CREDIT_MIX` | Variety of credit types (10%) |
| `NEW_CREDIT` | Recently opened accounts (10%) |

---

## Models

### CreditScore
**Credit score snapshot and factor breakdown.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `score_id` | `str` | *required* | Unique score record ID | Primary key |
| `user_id` | `str` | *required* | Score owner | Attribution |
| `score` | `int` | *required, 300-850* | Credit score value | Primary metric |
| `score_type` | `str` | `"fico"` | Score model: `FICO`, `VantageScore` | Model identification |
| `factors` | `Dict[str, float]` | `{}` | Factor impact scores | Breakdown analysis |
| `report_date` | `datetime` | *required* | When score was pulled | Freshness |
| `trend` | `str` | `"stable"` | Trend: `increasing`, `decreasing`, `stable` | Progress indicator |

---

### CreditRecommendation
**Actionable credit improvement suggestion.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `recommendation_id` | `str` | *required* | Unique recommendation ID | Tracking |
| `factor` | `CreditFactor` | *required* | Factor being addressed | Focus area |
| `title` | `str` | *required* | Recommendation headline | Display |
| `description` | `str` | *required* | Detailed explanation | User guidance |
| `impact_score` | `int` | *required* | Estimated points improvement | Prioritization |
| `difficulty` | `str` | *required* | Effort level: `easy`, `medium`, `hard` | User expectation |
| `estimated_time` | `str` | *required* | Time to see results: `1 month`, `3 months` | Timeline |
| `action_items` | `List[str]` | *required* | Specific steps to take | Actionable guidance |

---

### CreditProjection
**Projected future credit score.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `projection_id` | `str` | *required* | Unique projection ID | Tracking |
| `current_score` | `int` | *required* | Starting score | Baseline |
| `projected_score` | `int` | *required* | Expected future score | Goal setting |
| `projected_date` | `datetime` | *required* | When projection applies | Timeline |
| `assumptions` | `Dict` | *required* | Projection assumptions | Transparency |
| `confidence_level` | `float` | *required* | Projection confidence | Reliability indicator |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `CreditMonitoringService` | Score tracking |
| `CreditImprovementService` | Recommendation generation |
| `LinkedAccountService` | Credit bureau integration |

## Frontend Components
- Credit dashboard (FrontendCredit)
- Score history chart
- Factor breakdown pie chart
- Improvement action list
