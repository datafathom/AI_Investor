# Schema: Spending

## File Location
`schemas/spending.py`

## Purpose
Pydantic models for spending analysis and categorization including merchant mapping, spending patterns, and cashflow projections.

---

## Models

### SpendingTransaction
**Categorized spending transaction.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `transaction_id` | `str` | *required* | Transaction ID | Primary key |
| `user_id` | `str` | *required* | User | Attribution |
| `amount` | `float` | *required* | Transaction amount | Value |
| `merchant` | `str` | *required* | Merchant name | Categorization |
| `category` | `str` | *required* | Spending category | Analysis |
| `subcategory` | `Optional[str]` | `None` | Subcategory | Granular analysis |
| `date` | `datetime` | *required* | Transaction date | Timing |
| `account_id` | `str` | *required* | Source account | Account tracking |
| `is_recurring` | `bool` | `False` | Whether recurring | Pattern detection |

---

### SpendingPattern
**Detected spending pattern.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `pattern_id` | `str` | *required* | Pattern ID | Primary key |
| `user_id` | `str` | *required* | User | Attribution |
| `category` | `str` | *required* | Spending category | Classification |
| `average_amount` | `float` | *required* | Average spending | Baseline |
| `frequency` | `str` | *required* | Frequency: `daily`, `weekly`, `monthly` | Pattern |
| `day_of_week` | `Optional[int]` | `None` | Common day (0-6) | Pattern |
| `day_of_month` | `Optional[int]` | `None` | Common day (1-31) | Pattern |
| `merchant` | `Optional[str]` | `None` | Associated merchant | Pattern |

---

### CashflowProjection
**Projected cashflow.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `projection_id` | `str` | *required* | Projection ID | Primary key |
| `user_id` | `str` | *required* | User | Attribution |
| `month` | `str` | *required* | Month (YYYY-MM) | Period |
| `projected_income` | `float` | *required* | Expected income | Income |
| `projected_expenses` | `float` | *required* | Expected expenses | Outflow |
| `projected_net` | `float` | *required* | Net cashflow | Summary |
| `confidence_level` | `float` | *required* | Projection confidence | Quality |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `SpendingAnalysisService` | Transaction analysis |
| `PatternDetectionService` | Pattern recognition |
| `CashflowService` | Projections |
