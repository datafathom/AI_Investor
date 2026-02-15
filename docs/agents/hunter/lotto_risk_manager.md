# Lotto Risk Manager (Agent 7.4)

## ID: `lotto_risk_manager`

## Role & Objective
The 'Asymmetric Hedger'. Manages tiny positions with 100x potential and 100% loss probability. Ensures the 'Lotto' bucket doesn't bleed.

## Logic & Algorithm
- Enforces a 0.5% max allocation per 'Moonshot' asset.
- Automatically harvests 2x gains to recover initial principal.
- Monitors 'Total Loss' events to prune the portfolio of dead assets.

## Inputs & Outputs
- **Inputs**:
  - `high_risk_positions` (List): Tickers in the 'Lotto' category.
- **Outputs**:
  - `risk_adjusted_balance` (float): Total value of high-risk holdings.
  - `prune_recommendations` (List): Assets with zero remaining catalyst probability.

## Acceptance Criteria
- Rebalance the Lotto bucket weekly to ensure no single asset exceeds the 0.5% cap.
- Alert the Orchestrator immediately if the total Lotto bucket exceeds 5% of total portfolio equity.
