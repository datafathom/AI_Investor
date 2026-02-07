# Backend Service: Planning (The CFO)

## Overview
The **Planning Service** creates the roadmap for financial independence. It uses goal-based investing principles to reverse-engineer the required savings rates and asset allocations needed to hit specific life milestones (Retirement, Home Purchase, Philanthropy). It also includes a "Tough Love" module (`spending_analyzer.py`) to detect lifestyle creep.

## Core Components

### 1. Financial Planning Engine (`financial_planning_service.py`)
The Architect.
- **Goal Projection**: Calculates the future value of current savings + projected contributions to see if a goal is "On Track."
- **Asset Allocation**: Recommends a specific mix (Equity/Fixed Income/Cash) based on the *time horizon* of each goal (e.g., 80/20 for retirement in 20 years, but 20/80 for a house down payment in 2 years).
- **Contribution Optimization**: Solves for the *minimum* monthly savings needed to hit all goals, or prioritizes goals if capacity is limited.

### 2. Spending Analyzer (`spending_analyzer.py`)
The Auditor.
- **Waste Detection**: Flags spending categories that exceed peer-group benchmarks (e.g., "Dining > $1,000/mo") or indicate inefficiency (e.g., "Subscriptions > $200/mo").
- **Savings Rate Calculation**: Tracks the most important metric in personal finance: `(Savings / (Expenses + Savings))`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Financial Plan** | Goal Timeline | `financial_planning_service.project_goal_timeline()` | **Implemented** (`FinancialPlanningDashboard.jsx`) |
| **Zen Mode** | Retirement Gauge | `financial_planning_service` (Progress %) | **Implemented** (`RetirementGauge.jsx`) |
| **Cash Flow** | Spending Audit | `spending_analyzer.analyze_patterns()` | **Partially Implemented** (Mock logic in dashboard) |

## Dependencies
- `numpy`: Used for financial math (FV, PV, PMT functions).
- `schemas.financial_planning`: Pydantic models for strict type validation of financial goals.

## Usage Examples

### Creating a Retirement Plan
```python
from services.planning.financial_planning_service import get_financial_planning_service

planner = get_financial_planning_service()

# Define a goal: Retire with $5M in 20 years
plan = await planner.create_financial_plan(
    user_id="user_01",
    goals=[{
        "name": "Retirement",
        "target_amount": 5000000.0,
        "current_amount": 500000.0,
        "target_date": datetime(2046, 1, 1)
    }],
    monthly_contribution_capacity=10000.0
)

# Check if on track
projection = await planner.project_goal_timeline(plan.goals[0])
print(f"On Track: {projection.on_track}")
print(f"Projected Completion: {projection.projected_date}")
```

### Analyzing Monthly Spend
```python
from services.planning.spending_analyzer import SpendingAnalyzer
from schemas.spending import SpendingCategory

auditor = SpendingAnalyzer()

report = auditor.analyze_patterns(
    SpendingCategory(
        user_id="user_01",
        subscriptions=250.0, # Flagged as high
        food_dining=800.0,
        total_spending=8000.0,
        savings_contributions=2000.0
    )
)

print(f"Savings Rate: {report['savings_rate']:.1%}")
for opp in report['opportunities']:
    print(f"Alert: {opp['message']}")
```
