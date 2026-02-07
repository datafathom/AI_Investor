# Schema: Financial Plan

## File Location
`schemas/financial_plan.py`

## Purpose
Simplified Pydantic models for financial plan generation workflow. Represents a financial plan being generated for a user with complexity scoring and review requirements.

---

## Models

### FinancialPlanBase
**Base model for financial plan creation.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Plan owner | Attribution |
| `plan_type` | `str` | `"STANDARD"` | Type: `STANDARD`, `UHNW`, `SPECIALIZED` | Plan complexity |
| `complexity_score` | `float` | `0.0` | Computed complexity (0-100) | Pricing, routing |
| `status` | `str` | `"GENERATING"` | Status: `GENERATING`, `COMPLETE`, `REVIEW` | Workflow state |

---

### FinancialPlan
**Full financial plan record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `price` | `float` | `2500.0` | Plan price in dollars | Billing |
| `requires_human_review` | `bool` | `False` | Whether human review needed | Workflow routing |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

## Related Schema
See `financial_planning.py` for detailed goal-based planning models.

## Integration Points

| Service | Usage |
|---------|-------|
| `FinancialPlanService` | Plan generation |
| `ReviewService` | Human review workflow |
| `BillingService` | Plan pricing |
