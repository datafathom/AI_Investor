# Backend Service: Backtest

## Overview
The **Backtest Service** is a high-performance simulation engine designed to validate trading strategies against historical data. Built on top of the **Polars** library, it leverages vectorized, columnar operations to achieve sub-second execution speeds, even when processing decade-long datasets of 1-minute intervals.

## Core Components

### Polars Backtest Engine (`polars_backtest_engine.py`)
The primary engine for strategy simulation and performance metric calculation.

#### Classes

##### `PolarsBacktestEngine`
A singleton service that manages the execution of various quantitative strategies.

**Supported Strategies:**
- **SMA Crossover**: A classic trend-following strategy using fast and slow Simple Moving Averages.
- **Momentum Strategy**: Captures gains by following existing market trends based on lookback and holding periods.
- **Mean Reversion**: Uses Z-score thresholds to identify overextended price movements for potential reversals.

**Key Features:**
- **Vectorized Calculations**: Uses Polars rolling windows and columnar transformations to eliminate slow row-by-row iteration.
- **Memory Efficiency**: Ensures large data frames are discarded immediately after calculation to prevent memory bloat during batch simulations.
- **Performance**: Capable of executing a 10-year SMA crossover on 1-minute data in less than 2 seconds.

#### Data Models

##### `BacktestConfig`
Defines the parameters for a simulation run:
- `ticker`: The asset symbol.
- `initial_capital`: Starting bankroll (default: $100,000).
- `commission` & `slippage`: Friction modeling for realistic results.

##### `BacktestMetrics`
The structured output of a backtest, including:
- `total_return_pct` & `annualized_return_pct`.
- `sharpe_ratio`: Risk-adjusted return metric.
- `max_drawdown_pct`: Measures the largest peak-to-trough decline.
- `win_rate` & `profit_factor`.
- `execution_time_ms`: Engine performance measurement.

## Dependencies
- `polars`: The core high-performance data processing engine.
- `dataclasses`: Used for structured configuration and result objects.

## Usage Example

### Running a Fast SMA Crossover Backtest
```python
from services.backtest.polars_backtest_engine import get_backtest_engine, BacktestConfig

engine = get_backtest_engine()

config = BacktestConfig(
    strategy_name="QuickSMA",
    ticker="TSLA",
    start_date="2020-01-01",
    end_date="2024-12-31"
)

# Run the vectorized crossover
metrics = engine.run_sma_crossover(
    config=config,
    fast_period=20,
    slow_period=100
)

print(f"Total Return: {metrics.total_return_pct:.2f}%")
print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
print(f"Simulation completed in {metrics.execution_time_ms:.1f}ms")
```
