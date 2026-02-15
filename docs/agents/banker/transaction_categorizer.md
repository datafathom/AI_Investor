# Transaction Categorizer (Agent 18.1)

## ID: `transaction_categorizer`

## Role & Objective
The 'Ledger Clerk'. Automatically labels all system-wide financial movements (buy, sell, transfer, fee, tax, payroll) for institutional reporting and audit readiness.

## Logic & Algorithm
- **Pattern Matching**: Associates transaction descriptions with predefined categories using regex and historical mapping.
- **NLP Classification**: Uses LLM logic to classify ambiguous vendor names or unusual transaction strings.
- **Account Mapping**: Ensures every movement is correctly attributed to the right sub-account (e.g., "Trading" vs "Operational").

## Inputs & Outputs
- **Inputs**:
  - `raw_transaction_log` (Stream): ID, Date, Amount, Description.
- **Outputs**:
  - `categorized_ledger_entry` (JSON): Appended with `category_id` and `department_tag`.

## Acceptance Criteria
- Achieve 99% accuracy in categorizing recurring operational expenses.
- Tag and alert on "Unknown Vendor" events in < 1 second.
