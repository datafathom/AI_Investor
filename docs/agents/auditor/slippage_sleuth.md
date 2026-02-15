# Slippage Sleuth (Agent 12.1)

## ID: `slippage_sleuth`

## Role & Objective
The 'Execution Detective'. Compares intended fill price versus actual fill price for every trade to identify costly slippage and optimize order routing logic.

## Logic & Algorithm
- **Delta Analysis**: Calculates the difference between the "Order Sent" price and the "Execution Confirmed" price.
- **Venue Grading**: Ranks different brokerages and liquidity pools by their historical slippage profiles.
- **Alert Trigger**: Flags executions where slippage exceeds twice the expected volatility-adjusted variance.

## Inputs & Outputs
- **Inputs**:
  - `execution_confirmations` (List): Trade fill data.
  - `intended_order_logs` (List): The original trade requests.
- **Outputs**:
  - `slippage_report` (Dict): Realized slippage in basis points (BPS) per trade.

## Acceptance Criteria
- Identify and categorize slippage for 100% of executed trades.
- Notify the Strategist if any specific venue shows consistent slippage > 10% above the benchmark.
