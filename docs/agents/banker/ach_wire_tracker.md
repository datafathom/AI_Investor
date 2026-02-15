# ACH/Wire Tracker (Agent 18.2)

## ID: `ach_wire_tracker`

## Role & Objective
The 'Flow Watcher'. Monitors and confirms the status of all off-chain financial transfers (Bank to Exchange, Exchange to Bank, Wire to Counterparties).

## Logic & Algorithm
- **Status Polling**: Interfaces with bank API webhooks to track "Pending," "Clearing," and "Settled" states.
- **Reconciliation Check**: Verifies that the amount leaving the bank matches the amount arriving at the destination, minus fees.
- **Delay Warning**: Alerts the Sentry if a transfer exceeds the "Expected Settlement Window" (e.g., Wire > 24h, ACH > 3 days).

## Inputs & Outputs
- **Inputs**:
  - `transfer_orders` (List).
  - `bank_settlement_feeds` (Stream).
- **Outputs**:
  - `settlement_confirmation` (Status).

## Acceptance Criteria
- Confirm settling of 100% of initiated transfers.
- Trigger an "Institutional Delay Alert" if any wire is stuck for > 48 hours.
