# Liquidity Scout (Agent 5.4)

## ID: `liquidity_scout`

## Role & Objective
The "Depth Finder". Identifies the deepest pools of liquidity to ensure large orders are filled without causing significant market moving "impact".

## Logic & Algorithm
1. **Dark Pool Probing**: Checks for hidden liquidity in institutional venues.
2. **Market Impact Modeling**: Predicts how much a trade of size X will move the market price Y.
3. **Smart Routing**: Recommends the exact volume split across different exchanges to optimize the fill.

## Inputs & Outputs
- **Inputs**:
  - `prospective_order_size` (float): Total units to trade.
- **Outputs**:
  - `routing_recommendation` (List): % volume per venue.
  - `forecast_impact_bps` (float): Expected slippage.

## Acceptance Criteria
- Routing recommendations must be updated every 500ms during active trade execution.
- Maintain Impact Prediction accuracy to within 5 basis points of the actual outcome.
