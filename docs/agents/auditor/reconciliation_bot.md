# Reconciliation Bot (Agent 12.5)

## ID: `reconciliation_bot`

## Role & Objective
The 'Ledger Matcher'. Cross-references internal trading logs with institutional brokerage statements to find "Breaks" or discrepancies in shared state.

## Logic & Algorithm
- **Three-Way Match**: Compares the Orchestrator's intent, the Trader's logs, and the Broker's final settlement.
- **Settlement Tracking**: Monitors "T+1" or "T+2" settlement cycles to ensure cash availability for the Flow Master.
- **Discrepancy Resolution**: Flags "Phantom Positions" (stocks the system thinks it owns but the broker doesn't, or vice-versa).

## Inputs & Outputs
- **Inputs**:
  - `internal_ledger` (DB): The system's record of truth.
  - `external_settlement_data` (Stream): The broker's record of truth.
- **Outputs**:
  - `reconciliation_break_alert` (List): Identified mismatches.

## Acceptance Criteria
- Complete a full ledger reconciliation every 24 hours.
- Maintain a "zero-break" status for 100% of settled cash and securities.
