# Documentation: `tests/unit/test_backtest_agent.py`

## Overview
The Backtest Agent is the "Simulator" of the AI workforce. These tests ensure it can accurately run historical simulations and validate strategies against the system's "K-Factor" performance metric.

## Agent Under Test
- `agents.backtest_agent.BacktestAgent`

## Key Test Scenarios

### 1. Backtest Execution Lifecycle
- **Goal**: Verify structured command processing for simulations.
- **Assertions**:
    - `RUN_BACKTEST` returns a success action with calculated metrics (Return, Sharpe, K-Factor).
    - `GET_RESULTS` correctly retrieves the latest cached simulation results.

### 2. K-Factor Validation
- **Goal**: Use the K-Factor as a "Go/No-Go" gauge for strategy deployment.
- **Assertions**:
    - `DEPLOY` recommendation is issued if K-Factor exceeds the user's defined threshold.
    - `REJECT` recommendation is issued if the strategy fails to meet the performance floor.

### 3. Data Integrity
- **Goal**: Ensure the agent can consume historical price buckets.
- **Assertions**: `LOAD_DATA` correctly counts and confirms ingestion of symbol-specific historical records.

## Holistic Context
The Backtest Agent acts as a "Gatekeeper". By validating every strategy against historical data and the K-Factor metric, it ensures that the Sovereign OS only deploys capital to strategies that have a statistically proven edge.
