# Documentation: `tests/risk/test_stress_testing_service.py`

## Overview
This test suite validates the `StressTestingService`, which simulates how portfolios would perform under extreme market conditions, including historic crises and stochastic future projections.

## Service Under Test
- `services.risk.stress_testing_service.StressTestingService`

## Fixtures
- `service`: `StressTestingService` instance with the Monte Carlo engine and portfolio services mocked.

## Test Scenarios

### 1. Historical Crisis Simulations
- **Goal**: Replay historical "Black Swan" events against the current portfolio.
- **Assertions**:
    - `2008_financial_crisis`: Correctly calculates losses (~50% in mock).
    - `2020_covid_crash`: Correctly calculates losses (~35% in mock).
    - `2022_inflation_shock`: Correctly calculates losses (~20% in mock).

### 2. Stochastic Simulations (Monte Carlo)
- **Goal**: Generate 10,000+ random future paths to determine the probability of various outcomes.
- **Assertions**:
    - Result is a `MonteCarloResult` schema.
    - Expected values and horizons match input parameters (e.g., 252-day horizon).
    - Handles small sample sizes and different time horizons (30-365 days) correctly.

### 3. Custom Scenarios and Boundary Conditions
- **Goal**: Allow users to define their own shocks and ensure the system handles edge cases.
- **Assertions**:
    - Correctly calculates loss for custom `StressScenario` objects.
    - Gracefully handles zero-value portfolios (returns 0% loss).
    - Raises `ValueError` for unknown or invalid scenario names.

## Holistic Context
Stress testing is mandatory for institutional-grade risk management. These tests guarantee that the system can reliably answer the question "What happens if the market crashes like 2008 today?", providing users with essential peace of mind.
