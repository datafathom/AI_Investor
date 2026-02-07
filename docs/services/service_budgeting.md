# Backend Service: Budgeting

## Overview
The **Budgeting Service** provides the financial planning and discipline layer for the Sovereign OS. It enables users to set structured spending goals, automatically categorize real-world expenses, and receive analytical insights into their spending trends and budget compliance.

## Core Components

### 1. Budget Orchestrator (`budgeting_service.py`)
Manages the lifecycle of multiple concurrent budgets (e.g., "Monthly Operations," "Personal Surplus").
- **Dynamic Allocation**: Supports defining budgets across 10+ categories (Housing, Transport, Food, etc.) for specific time periods.
- **Delta Analysis**: Compares `total_budgeted` vs `total_spent` in real-time, providing actionable metrics like `remaining_balance` and identifying over-budget "problem categories."

### 2. Expense Tracking Engine (`expense_tracking_service.py`)
The transactional intake system for the budgeting framework.
- **Auto-Categorization**: Uses a sophisticated keyword-based matching engine to automatically assign transactions to categories (e.g., "Starbucks" -> "Food," "Mortgage" -> "Housing").
- **Spending Insights**: Calculates total spending velocity over rolling 30-day windows.
- **Trend Analysis**: Monitors spending behavior over a 90-day window to detect if a category is "Increasing," "Stable," or "Decreasing" in cost.

## Categories Supported
The system uses the `ExpenseCategory` schema to track:
- **Core Essentials**: Housing, Utilities, Healthcare, Insurance.
- **Lifestyle**: Transportation, Food, Entertainment, Shopping.
- **Financial Strategy**: Debt (loan payments), Education, and Other.

## Dependencies
- `pydantic`: Defines the `Budget`, `Expense`, and `SpendingTrend` data models.
- `services.system.cache_service`: For rapid persistence and retrieval of spending history.
- `datetime`: Manages all period-based analysis for monthly and annual trends.

## Usage Examples

### Creating a Monthly Personal Budget
```python
from services.budgeting.budgeting_service import get_budgeting_service

budget_service = get_budgeting_service()

# Define categories and limits
limits = {
    "housing": 3000.00,
    "food": 800.00,
    "transportation": 400.00,
    "entertainment": 200.00
}

budget = await budget_service.create_budget(
    user_id="user_vanguard_1",
    budget_name="Feb_2026_Baseline",
    period="monthly",
    categories=limits
)

print(f"Budget Created: {budget.budget_id} (Total: ${budget.total_budget:,.2f})")
```

### Analyzing Spending Against Budget
```python
from services.budgeting.budgeting_service import get_budgeting_service

budget_service = get_budgeting_service()

analysis = await budget_service.get_budget_analysis(
    budget_id="budget_user_vanguard_1_123456789"
)

print(f"Total Spent: ${analysis.total_spent:,.2f}")
print(f"Remaining: ${analysis.remaining:,.2f}")

if analysis.over_budget_categories:
    print(f"CRITICAL: Over budget in {', '.join(analysis.over_budget_categories)}")
```
