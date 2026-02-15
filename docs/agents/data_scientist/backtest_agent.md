# Backtest Agent (`backtest_agent.py`)

## Description
The `BacktestAgent` is the primary validator for trading strategies. It runs historical simulations on OHLCV data to calculate performance metrics and ensure a strategy is viable before deployment.

## Role in Department
It serves as the final barrier in the Quant Lab (Strategist department), providing the "K-Factor" validation required by the Sovereign OS roadmap.

## Input & Output
- **Input**: Strategy definition, date range, initial capital, and ticker symbol.
- **Output**: `BacktestResult` including Sharpe Ratio, Max Drawdown, Win Rate, and the critical `k_factor`.

## Pipelines & Integration
- **Database**: Pulls historical time-series data from Postgres.
- **Monte Carlo**: Provides data for k-factor validation (k > 1.05 required for deployment).
- **Execution Workflow**: Signals from the `Strategist` department are routed here for historical verification.

## Key Metrics
- **K-Factor**: A multiplier representing profit expectancy. Sustainable growth requires `k > 1.0`.
- **Max Drawdown**: Crucial for ensuring the strategy doesn't violate tail-risk constraints.
