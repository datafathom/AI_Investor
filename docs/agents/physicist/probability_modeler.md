# Probability Modeler (Agent 6.5)

## ID: `probability_modeler`

## Role & Objective
The "System Odds-Maker". This agent uses advanced statistical distributions to calculate the exact probability of specific financial outcomes.

## Logic & Algorithm
1. **Distribution Selection**: Utilizes Log-Normal and Cauchy distributions to model asset returns, accounting for "Fat Tails".
2. **EV Assessment**: Calculates the Expected Value (EV) for every open trade idea produced by the Strategist department.
3. **Profit Visibility**: Generates Probability of Profit (POP) and Probability of Touch (POT) metrics for the front-end dashboard.

## Inputs & Outputs
- **Inputs**:
  - `ticker_history` (List): Returns data for distributional fit.
  - `option_ivs` (float): The market's forward-looking volatility.
- **Outputs**:
  - `p_hit_target` (float): Probability of price reaching X by date Y.
  - `expected_move_1sd` (float): Statistically anticipated price range.

## Acceptance Criteria
- Calculate 1,000+ Monte Carlo price paths for an asset in under 1 second.
- Probability projections must align with historical realized outcomes within a 5% margin of error.
