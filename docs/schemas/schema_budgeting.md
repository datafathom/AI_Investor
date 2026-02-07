# Schema: Budgeting

## File Location
`schemas/budgeting.py`

## Purpose
Pydantic models for personal budgeting, expense tracking, and spending analysis. Enables users to create budgets, categorize expenses, and analyze spending patterns against budget targets.

---

## Enums

### ExpenseCategory
**Standard expense categorization.**

| Value | Description |
|-------|-------------|
| `HOUSING` | Rent, mortgage, property taxes |
| `TRANSPORTATION` | Car payments, gas, transit |
| `FOOD` | Groceries and dining |
| `UTILITIES` | Electric, water, internet |
| `INSURANCE` | Health, auto, life insurance |
| `HEALTHCARE` | Medical expenses, prescriptions |
| `ENTERTAINMENT` | Movies, subscriptions, hobbies |
| `SHOPPING` | Retail purchases |
| `EDUCATION` | Tuition, books, courses |
| `SAVINGS` | Transfers to savings |
| `DEBT` | Debt payments |
| `OTHER` | Uncategorized expenses |

---

## Models

### Budget
**User budget definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `budget_id` | `str` | *required* | Unique budget identifier | Primary key |
| `user_id` | `str` | *required* | Budget owner | Access control |
| `budget_name` | `str` | *required* | User-defined name | Display |
| `period` | `str` | *required* | Period: `monthly`, `yearly` | Time frame |
| `categories` | `Dict[str, float]` | *required* | Category budgets: `{category: amount}` | Budget allocation |
| `total_budget` | `float` | *required* | Sum of all category budgets | Total spending limit |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### Expense
**Individual expense transaction.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `expense_id` | `str` | *required* | Unique expense identifier | Primary key |
| `user_id` | `str` | *required* | Expense owner | Access control |
| `amount` | `float` | *required* | Expense amount | Financial tracking |
| `category` | `ExpenseCategory` | *required* | Expense category | Budget mapping |
| `description` | `str` | *required* | What the expense was for | Context |
| `merchant` | `Optional[str]` | `None` | Where the expense occurred | Merchant analytics |
| `date` | `datetime` | *required* | When expense occurred | Time-based analysis |
| `account_id` | `Optional[str]` | `None` | Source account | Account reconciliation |
| `receipt_url` | `Optional[str]` | `None` | Receipt image URL | Documentation |

---

### BudgetAnalysis
**Budget vs. actual spending analysis.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `budget_id` | `str` | *required* | Associated budget | Links to budget |
| `period_start` | `datetime` | *required* | Analysis period start | Time window |
| `period_end` | `datetime` | *required* | Analysis period end | Time window |
| `total_budgeted` | `float` | *required* | Total budget for period | Budget baseline |
| `total_spent` | `float` | *required* | Total actual spending | Reality |
| `remaining` | `float` | *required* | Remaining budget | Available funds |
| `category_analysis` | `Dict[str, Dict]` | *required* | Per-category breakdown: `{budgeted, spent, remaining, percentage}` | Category detail |
| `over_budget_categories` | `List[str]` | *required* | Categories exceeding budget | Alert triggers |
| `under_budget_categories` | `List[str]` | *required* | Categories under budget | Savings opportunities |

---

### SpendingTrend
**Spending trend analysis over time.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `category` | `str` | *required* | Expense category | Categorization |
| `period` | `str` | *required* | Analysis period | Time frame |
| `average_spending` | `float` | *required* | Average spending amount | Baseline |
| `trend_direction` | `str` | *required* | Direction: `increasing`, `decreasing`, `stable` | Trend indicator |
| `percentage_change` | `float` | *required* | Change percentage | Trend magnitude |
| `forecast` | `Optional[float]` | `None` | Predicted next period spending | Planning |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `BudgetingService` | Budget CRUD operations |
| `ExpenseTrackingService` | Transaction categorization |
| `SpendingAnalysisService` | Trend analysis and forecasting |
| `LinkedAccountService` | Automatic expense import |

## Frontend Components
- Budget dashboard (FrontendBudget)
- Expense entry forms
- Category pie charts
- Trend line graphs
