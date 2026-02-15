# Fee Forensic Agent (Agent 12.4)

## ID: `fee_forensic_agent`

## Role & Objective
The 'Leakage Finder'. Scans institutional statements for incorrect commission tiering, hidden fees, or "PFOF" (Payment for Order Flow) leakage.

## Logic & Algorithm
- **Commission Audit**: Compares actual fees charged against the brokerage's published "Active Trader" tiered schedule.
- **Hidden Fee Detection**: Identifies "SEC Fees" or "ADR Fees" that weren't disclosed in the pre-trade estimates.
- **Arbitrage Check**: Verifies that the Flow Master's sweeps aren't being offset by excessive transfer fees.

## Inputs & Outputs
- **Inputs**:
  - `brokerage_statements` (PDF/Data): Institutional billing documents.
- **Outputs**:
  - `fee_leakage_report` (float): Total USD lost to excessive or incorrect fees.

## Acceptance Criteria
- Reconcile 100% of trading commissions against the published tier schedule.
- Identify overcharges of > $5 within 30 days for recovery requests.
