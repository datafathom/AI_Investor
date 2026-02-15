# Position Sizer (Agent 5.5)

## ID: `position_sizer`

## Role & Objective
The "Kelly Criterion" engine. Determines exactly how much capital to risk on a single trade based on the edge (confidence) and the current market volatility.

## Logic & Algorithm
1. **Fractional Kelly**: Applies the Kelly Criterion to signals to find the optimal growth-maximizing size.
2. **Risk Capping**: Enforces strict "Max 2% Risk" rules per trade relative to total portfolio equity.
3. **Exposure Correlation**: Checks if the new trade increases "Sector Over-exposure" (e.g., too much Tech) and reduces size accordingly.

## Inputs & Outputs
- **Inputs**:
  - `trade_signal` (Dict): Direction and confidence.
  - `current_portfolio_equity` (float): Total liquid capital.
- **Outputs**:
  - `recommended_qty` (float): Number of units to buy.
  - `ruin_probability` (float): Risk assessment.

## Acceptance Criteria
- 100% of trades must pass through the Position Sizer before being sent to the Sniper.
- Never exceed the 2% maximum risk-per-trade cap under any circumstances.
