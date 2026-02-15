# Margin Call Watchdog (Agent 18.5)

## ID: `margin_call_watcher`

## Role & Objective
The 'Liquidator's Nemesis'. Monitors exchange-level margin requirements for leveraged positions to prevent the catastrophic "Forced Closing" of trades by brokers.

## Logic & Algorithm
- **Threshold Escalation**:
    - **Level 1 (Alert)**: 20% margin usage.
    - **Level 5 (Action Required)**: 50% margin usage.
    - **Level 9 (Immediate Panic)**: 80% margin usage.
- **Equity Projection**: Uses the Physicist's probability models to predict the likelihood of hitting a margin call within the next 4 hours.

## Inputs & Outputs
- **Inputs**:
  - `exchange_margin_data` (API): Maintenance, Initial, and Current Equity.
- **Outputs**:
  - `margin_health_alert` (List): Tickers at risk of forced liquidation.

## Acceptance Criteria
- Trigger a "Level 9" alert 100% of the time before an actual margin call occurs.
- Maintain a margin-usage history that is accessible to the Auditor for "Behavioral Analysis."
