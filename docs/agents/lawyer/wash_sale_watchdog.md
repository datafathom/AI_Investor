# Wash-Sale Watchdog (Agent 11.1)

## ID: `wash_sale_watchdog`

## Role & Objective
The 'Tax Guard'. Blocks trades that would trigger wash-sale tax violations (selling at a loss and rebuying within 30 days), protecting the portfolio's after-tax returns.

## Logic & Algorithm
- **Rebuy Monitoring**: Scans all realized losses from the last 30 days for any asset.
- **Trade Blocking**: Issues a "DENY" signal to the Trader department if a buy order is attempted for a recently sold losing position.
- **Replacement Sourcing**: Suggests similar but non-identical assets (e.g., a different ETF in the same sector) to maintain exposure without triggering the rule.

## Inputs & Outputs
- **Inputs**:
  - `realized_loss_history` (Dict): Tickers and dates of recent losses.
  - `pending_buy_orders` (List): Orders queued for execution.
- **Outputs**:
  - `compliance_decision` (Allow/Block): Permission status for each trade.

## Acceptance Criteria
- Block 100% of wash-sale violations across all connected brokerage accounts.
- Provide a "Replacement Asset" recommendation for 90% of blocked trades.
