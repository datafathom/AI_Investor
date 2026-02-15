# Opportunity Screener (Agent 4.4)

## ID: `opportunity_screener`

## Role & Objective
The "Watchlist Filter". Scans the entire asset universe (Top 500+) for specific technical or fundamental setups that match the current strategy playbook.

## Logic & Algorithm
1. **Parallel Screening**: Applies Logic Architect filters across thousands of ticker data points.
2. **Alpha Ranking**: Ranks matching assets by their expected risk-adjusted return (Sharpe expectancy).
3. **Signal Guarding**: Flags high-conviction signals to the Orchestrator for human-in-the-loop approval.

## Inputs & Outputs
- **Inputs**:
  - `universe_data` (List): Price and volume snapshots for symbols.
  - `screen_criteria` (Dict): Multi-factor filters (PE, RSI, Momentum).
- **Outputs**:
  - `filtered_watchlist` (List): Tickers meeting criteria, ranked by score.

## Acceptance Criteria
- Screen 500+ symbols against 5+ technical criteria in under 1 second.
- False positive rate for signal detection must be < 5% when compared to backtest logic.
