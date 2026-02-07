# Documentation: `tests/risk/test_advanced_risk_metrics_service.py`

## Overview
This test suite provides exhaustive coverage for the `AdvancedRiskMetricsService`. It validates the calculation of crucial risk indicators across multiple methodologies (Historical, Parametric, and Monte Carlo).

## Service Under Test
- `services.risk.advanced_risk_metrics_service.AdvancedRiskMetricsService`

## Fixtures
- `service`: `AdvancedRiskMetricsService` instance with dependencies like Monte Carlo Engine and Portfolio Aggregator mocked.
- `mock_returns`: A numpy array of simulated portfolio returns for arithmetic validation.

## Test Scenarios

### 1. Calculation Methodologies (Historical, Parametric, Monte Carlo)
- **Goal**: Verify that the service can calculate metrics using all three supported statistical methods.
- **Assertions**:
    - Result is a `RiskMetrics` schema object.
    - Fields like `var_95`, `var_99`, `cvar_95`, and `sharpe_ratio` are correctly populated.
    - The `method` field in the result matches the requested methodology.

### 2. Individual Metric Calculations
- **Goal**: Unit test the internal private methods for specific ratios.
- **Assertions**:
    - `_calculate_var` and `_calculate_cvar`: 99% values are logically $\ge$ 95% values.
    - `_calculate_max_drawdown`: Returns positive drawdown and non-negative duration.
    - `_calculate_sharpe_ratio`, `_calculate_sortino_ratio`, `_calculate_calmar_ratio`: Return valid numeric results.

### 3. Caching and Error Handling
- **Goal**: Ensure performance optimization via caching and robust failure modes.
- **Assertions**:
    - Returns cached data if available, bypassing expensive re-calculation.
    - Raises appropriate exceptions on empty return sets or database failures.

## Holistic Context
Risk metrics are the "vitals" of an investment portfolio. These tests ensure that the mathematical foundations of the platform are sound, preventing flawed data from being used in critical trade or rebalancing decisions.
