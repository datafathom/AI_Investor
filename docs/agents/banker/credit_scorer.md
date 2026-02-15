# Credit Scorer (Agent 18.4)

## ID: `credit_scorer`

## Role & Objective
The 'Internal Rating' agency. Assigns a proprietary credit score to the system's own sub-wallets and internal departments to manage capital allocation and risk limits.

## Logic & Algorithm
- **Repayment Profiling**: Tracks how quickly departments (Trader, Hunter) return borrowed capital to the central treasury.
- **Loss Magnitude Correlation**: Penalizes credit scores for departments that experience "Max Drawdown" events.
- **Limit Adjustment**: Automatically raises or lowers "Borrowing Caps" based on the department's rolling 90-day credit score.

## Inputs & Outputs
- **Inputs**:
  - `internal_ledger_history` (Dict): Inter-departmental loans and returns.
- **Outputs**:
  - `department_credit_score` (int): 300 to 850 range.

## Acceptance Criteria
- Maintain an updated credit score for all 18 departments every 30 days.
- Reduce "Capital Allocation" for any department whose credit score drops below 600.
