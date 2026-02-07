# Documentation: `tests/unit/test_monte_carlo.py`

## Overview
The Monte Carlo engine is responsible for predictive risk modeling. These tests ensure the simulation matches statistical distributions and meets institutional performance targets.

## Component Under Test
- `services.analysis.monte_carlo.MonteCarloEngine`

## Key Test Scenarios

### 1. Statistical Distributions
- **Goal**: Verify that simulations can follow Normal and Student-T distributions.
- **Assertions**: Generated paths match the expected shape (n_simulations x n_days) and correctly initialize all paths at the starting capital level.

### 2. Risk Metrics (VaR/CVaR)
- **Goal**: Verify Value-at-Risk and Conditional Value-at-Risk calculations.
- **Assertions**:
    - CVaR (Expected Shortfall) is correctly identified as being more severe than VaR.
    - Reproducibility is verified via Random Seeding—identical seeds must produce identical paths.

### 3. Performance Criteria (Acceptance C2)
- **Goal**: Ensure 10,000 simulations complete in < 5 seconds.
- **Assertions**: The test times the execution and asserts `True` only if the performance target is met.

## Holistic Context
Monte Carlo simulations allow the Sovereign OS to "dream" thousands of possible futures every night. These tests prove that those futures are statistically valid and that the "dreaming" process is fast enough for real-time risk adjustments.
