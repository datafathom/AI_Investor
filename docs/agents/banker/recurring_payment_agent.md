# Recurring Payment Agent (Agent 18.4)

## ID: `recurring_payment_agent`

## Role & Objective
The 'Auto-Payer'. Handles the reliable execution of monthly subscriptions, infrastructure costs, payroll, and other scheduled institutional outflows.

## Logic & Algorithm
- **Schedule Management**: Maintains a chronological calendar of all upcoming liabilities.
- **Liquidity Check**: Notifies the Liquidity Provider 48 hours before a large recurring payment to ensure cash-on-hand.
- **Execution Proof**: Collects and archives PDF receipts for every automated payment made.

## Inputs & Outputs
- **Inputs**:
  - `payment_schedule` (List): Recipient, Amount, Frequency, NextDate.
- **Outputs**:
  - `execution_receipt` (URI).

## Acceptance Criteria
- Achieve a 0% failure rate for critical infrastructure payments (Cloud, Data Feeds).
- Maintain 100% receipt coverage for all automated outflows.
