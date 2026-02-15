# Envelope Budget Manager (Agent 18.3)

## ID: `envelope_budget_manager`

## Role & Objective
The 'Allocater'. Manages the digital 'Envelope' system, ensuring that cash is precisely allocated across different institutional needs (e.g., "Market Opportunities," "Tax Reserves," "Payroll").

## Logic & Algorithm
- **Cash Partitioning**: Divides the total liquid treasury into virtual buckets based on the Architect's priority models.
- **Overrun Protection**: Blocks transactions from an "Envelope" if it has insufficient funds, requiring a "Re-allocation Request."
- **Sweep Logic**: Automatically moves surplus yield-earnings into the "Main Opportunity" envelope.

## Inputs & Outputs
- **Inputs**:
  - `treasury_balance` (float).
  - `allocation_weights` (Dict).
- **Outputs**:
  - `envelope_state_report` (JSON): Current balances across all digital envelopes.

## Acceptance Criteria
- Maintain 100% partitioning of assets with zero "Orphaned Cash."
- Block 100% of out-of-budget transaction attempts without a valid override.
