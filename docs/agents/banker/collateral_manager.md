# Collateral Manager (Agent 18.2)

## ID: `collateral_manager`

## Role & Objective
The 'Asset Guard'. Monitors the real-time value of assets pledged against loans and proactively manages collateral levels to prevent forced liquidations.

## Logic & Algorithm
- **Mark-to-Market Monitoring**: Tracks live price feeds for all collateralized tokens or stocks.
- **Health Factor Calculation**: Generates a continuous score representing the distance to a "Margin Call".
- **Auto-Injection**: Triggers "Emergency Re-collateralization" by moving stablecoins into the collateral vault if values drop > 10% in 1 hour.

## Inputs & Outputs
- **Inputs**:
  - `collateral_basket` (Dict): Tickers and Quantities pledged.
  - `active_debt_stream` (float): Total USD owed across all venues.
- **Outputs**:
  - `health_factor` (float): 1.0 (Danger) to 3.0+ (Safe).
  - `collateral_delta` (float): Required asset injection to stabilize loans.

## Acceptance Criteria
- Maintain all "Health Factors" above 1.5 during market volatility < 20%.
- Alert the user to "Strategic De-leveraging" if collateral value drops > 15% in a single day.
