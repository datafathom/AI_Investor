# Rebalance Bot (Agent 4.3)

## ID: `rebalance_bot`

## Role & Objective
The "Portfolio Gardener". The Rebalance Bot ensures the portfolio stays within its target strategic allocation bands, managing drift and maintaining the intended risk profile.

## Logic & Algorithm
1. **Drift Assessment**: Compares current asset weights in the ledger against the target model.
2. **Trade Generation**: Calculates the exact buy/sell orders needed to return to the target allocation.
3. **Tax Optimization**: Prioritizes tax-loss harvesting during the exit of overweight positions.

## Inputs & Outputs
- **Inputs**:
  - `target_weights` (Dict): Ideal asset percentage breakdown.
  - `live_positions` (Dict): Current portfolio held in the ledger.
- **Outputs**:
  - `rebalance_orders` (List): specific trade requests.
  - `drift_delta` (float): Total percentage variance from the model.

## Acceptance Criteria
- Trigger rebalance notifications within 60 seconds of any asset drifting more than 2.5% from its target.
- Trade generation must minimize transaction costs by aggregation across accounts.
