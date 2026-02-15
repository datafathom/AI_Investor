# Backtest Autopilot (Agent 3.2)

## ID: `backtest_autopilot`

## Role & Objective
Historical simulation engine. Validates trade strategies against Postgres OHLCV data.

## Logic & Algorithm
- Loads historical time-series data.
- Executes 'Mock Trades' based on strategy parameters.
- Calculates k-factor, Sharpe ratio, and Max Drawdown.

## Inputs & Outputs
- **Inputs**:
  - `strategy_id` (str): Reference to the logic being tested.
  - `date_range` (Tuple): Start and end dates for the simulation.
- **Outputs**:
  - `performance_report` (Dict): Metrics and equity curve.
  - `k_factor` (float): Profit expectancy multiplier (Roadmap criteria: k > 1.0).

## Acceptance Criteria
- Simulation of 5 years of daily data must complete in under 5 seconds.
- Resulting metrics must match a manual Excel-based validation to within 0.001%.
