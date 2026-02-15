# Black Swan Insurance Agent (Agent 6.6)

## ID: `black_swan_insurance_agent`

## Role & Objective
The "Tail-Risk Specialist". This agent manages the defensive layer of the portfolio, ensuring protection against rare, catastrophic market events.

## Logic & Algorithm
1. **Protection Sourcing**: Allocates a fixed monthly budget to deep Out-of-the-Money (OTM) protective options.
2. **Rolling Coverage**: Ensures there are no gaps in insurance coverage as options approach expiration.
3. **Budget Optimization**: Aggressively buys tail-protection when Implied Volatility (IV) is at historical lows (Cheap Insurance).

## Inputs & Outputs
- **Inputs**:
  - `portfolio_value` (float): Total AUM for sizing.
  - `insurance_budget` (float): Max allowed monthly premium spend.
- **Outputs**:
  - `insurance_status` (COVERED/UNINSURED).
  - `payout_at_minus_25pct` (float): Projected USD gain in a crash scenario.

## Acceptance Criteria
- 100% portfolio coverage against any single-day market drop exceeding 15%.
- Maintain an "insurance premium" spend of < 1.5% of total portfolio equity per annum.
