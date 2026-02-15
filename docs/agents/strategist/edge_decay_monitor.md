# Edge Decay Monitor (Agent 4.5)

## ID: `edge_decay_monitor`

## Role & Objective
The "Strategy Auditor". Monitors live performance vs historical expectations to detect "Alpha Decay"—the statistical vanishing of a trading edge.

## Logic & Algorithm
1. **Benchmarking**: Compares current Sharpe/Sortino ratios against the strategy's historical backtest performance.
2. **Regime Detection**: Identifies if the current market environment (e.g., high volatility) has shifted away from the strategy's profitable regime.
3. **Retirement Sentinel**: Issues automated warnings to de-risk or retire strategies that are failing to meet statistical benchmarks.

## Inputs & Outputs
- **Inputs**:
  - `live_performance` (Dict): Recent P&L and reward stats.
  - `historical_expectations` (Dict): Backtest baseline.
- **Outputs**:
  - `decay_status` (STABLE/DEGRADING/FAILED).
  - `retirement_alert` (bool): Flag to halt the strategy.

## Acceptance Criteria
- Issue a 'DEGRADING' warning if a strategy underperforms its backtest mean by 1 standard deviation for 30 consecutive days.
- Detect regime shifts within 5 trading days of a fundamental market character change.
