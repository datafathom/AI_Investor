# Schema: Financial Planning

## File Location
`schemas/financial_planning.py`

## Purpose
Comprehensive Pydantic models for goal-based financial planning including financial goals, projections, asset allocation recommendations, and complete financial plans.

---

## Enums

### GoalType
**Types of financial goals.**

| Value | Description |
|-------|-------------|
| `RETIREMENT` | Retirement savings goal |
| `HOUSE` | Home purchase goal |
| `EDUCATION` | Education funding goal |
| `VACATION` | Vacation savings |
| `EMERGENCY_FUND` | Emergency fund target |
| `DEBT_PAYOFF` | Debt elimination goal |
| `CUSTOM` | User-defined goal |

---

### GoalStatus
**Goal progress status.**

| Value | Description |
|-------|-------------|
| `NOT_STARTED` | Goal not yet started |
| `IN_PROGRESS` | Actively saving |
| `ON_TRACK` | Meeting projections |
| `AT_RISK` | Behind schedule |
| `COMPLETED` | Goal achieved |

---

## Models

### FinancialGoal
**Individual financial goal definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `goal_id` | `str` | *required* | Unique goal identifier | Primary key |
| `user_id` | `str` | *required* | Goal owner | Attribution |
| `goal_name` | `str` | *required* | User-defined name | Display |
| `goal_type` | `GoalType` | *required* | Goal category | Classification |
| `target_amount` | `float` | *required* | Target dollar amount | Goal target |
| `current_amount` | `float` | `0.0` | Current progress | Tracking |
| `target_date` | `datetime` | *required* | Goal deadline | Timeline |
| `priority` | `int` | `5` | Priority (1-10 scale) | Goal ranking |
| `status` | `GoalStatus` | `NOT_STARTED` | Current status | Progress tracking |
| `monthly_contribution` | `Optional[float]` | `None` | Planned monthly savings | Contribution planning |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### GoalProjection
**Projection analysis for a goal.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `goal_id` | `str` | *required* | Associated goal | Links to goal |
| `current_amount` | `float` | *required* | Current progress | Starting point |
| `target_amount` | `float` | *required* | Goal target | Endpoint |
| `projected_amount` | `float` | *required* | Projected final amount | Forecast |
| `projected_date` | `datetime` | *required* | Expected completion | Timeline |
| `months_to_completion` | `int` | *required* | Months remaining | Duration |
| `required_monthly_contribution` | `float` | *required* | Needed monthly amount | Guidance |
| `on_track` | `bool` | *required* | Whether meeting target | Status |
| `confidence_level` | `float` | *required, 0-1* | Projection confidence | Reliability |

---

### AssetAllocationRecommendation
**Recommended asset allocation for a goal.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `goal_id` | `str` | *required* | Associated goal | Links to goal |
| `recommended_allocation` | `Dict[str, float]` | *required* | Asset class weights | Portfolio construction |
| `risk_level` | `str` | *required* | Risk profile: `conservative`, `moderate`, `aggressive` | Risk matching |
| `expected_return` | `float` | *required* | Expected annual return | Projection input |
| `expected_volatility` | `float` | *required* | Expected standard deviation | Risk disclosure |
| `rationale` | `str` | *required* | Explanation for recommendation | Transparency |

---

### FinancialPlan (Extended)
**Complete multi-goal financial plan.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `plan_id` | `str` | *required* | Unique plan identifier | Primary key |
| `user_id` | `str` | *required* | Plan owner | Attribution |
| `goals` | `List[FinancialGoal]` | *required* | All financial goals | Goal aggregation |
| `total_target_amount` | `float` | *required* | Sum of all goal targets | Summary metric |
| `total_current_amount` | `float` | *required* | Sum of current progress | Summary metric |
| `monthly_contribution_capacity` | `float` | *required* | Available monthly savings | Constraint |
| `recommended_allocations` | `Dict[str, AssetAllocationRecommendation]` | *required* | Per-goal allocations | Portfolio guidance |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `FinancialPlanningService` | Plan management |
| `GoalTrackingService` | Progress monitoring |
| `ProjectionService` | Future projections |
| `AssetAllocationService` | Portfolio recommendations |

## Frontend Components
- Planning dashboard (FrontendPlanning)
- Goal progress trackers
- Projection charts
- Allocation visualizations
