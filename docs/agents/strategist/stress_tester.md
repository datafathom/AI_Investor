# Stress Tester (Agent 4.2)

## ID: `stress_tester`

## Role & Objective
The "Adversarial Agent". The Stress Tester subjects strategies to artificial market shocks and liquidity droughts to identify their "Burst Point".

## Logic & Algorithm
1. **Monte Carlo Attack**: Runs historical simulations with 'fat tail' risk parameters (rare but extreme events).
2. **Shocks Injection**: Simulates specific trauma (Credit Crunch, Flash Crash, Hyperinflation).
3. **Fragility Analysis**: Calculates the drawdown levels and likelihood of portfolio wipeout.

## Inputs & Outputs
- **Inputs**:
  - `baseline_strategy` (Dict): The strategy blueprint to attack.
  - `shock_vectors` (List): Types of market trauma to simulate.
- **Outputs**:
  - `fragility_report` (Dict): failure modes and max drawdown projections.
  - `survival_probability` (float): Likelihood of surviving a decade of volatility.

## Acceptance Criteria
- Fragility reports must identify the exact asset price move that results in a 50%+ drawdown.
- Survival probability calculations must be accurate to within 1% based on historical fat-tail distributions.
