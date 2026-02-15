# Life-Cycle Modeler (Agent 2.1)

## ID: `life_cycle_modeler`

## Role & Objective
The "North Star" of the Sovereign OS. The Life-Cycle Modeler is responsible for long-term financial forecasting and determining the exact moment of Financial Independence (FI). It models wealth accumulation over a 40-50 year horizon.

## Logic & Algorithm
1. **Simulation Engine**: Uses the `LifeCycleService` to run deterministic and Monte Carlo simulations of net worth growth.
2. **Burn Rate Analysis**: Factors in inflation-adjusted living expenses.
3. **Success Rate Calculation**: Determines the probability that the current investment strategy will sustain the user through retirement without depleting the principal.

## Inputs & Outputs
- **Inputs**:
  - Current Net Worth
  - Monthly Savings & Burn Rate
  - Expected Portfolio Return
  - Inflation Assumptions
- **Outputs**:
  - FI Year & Age
  - Portfolio Success Rate (%)

## Acceptance Criteria
- FI projections must update in under 1 second during live parameter adjustments.
- Monte Carlo simulations must run at least 1,000 iterations for statistical significance.
