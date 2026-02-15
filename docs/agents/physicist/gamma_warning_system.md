# Gamma Warning System (Agent 6.3)

## ID: `gamma_warning_system`

## Role & Objective
The "Market Acceleration Monitor". Detects when large price swings are being forced by the institutional need to hedge large option positions (Dealer Gamma).

## Logic & Algorithm
1. **Net Gamma Calculation**: Aggregates open interest to estimate the combined hedging requirement of market makers.
2. **Pin Detection**: Identifies specific "Magnetic" strikes (Pins) where price is likely to settle during monthly opex.
3. **Acceleration Alerts**: Warns when the market enters "Short Gamma" regimes, where volatility is likely to become convex and explosive.

## Inputs & Outputs
- **Inputs**:
  - `open_interest_data` (Dict): Exchange-wide OI snapshots.
  - `current_market_price` (float): Underlying spot price.
- **Outputs**:
  - `gamma_exposure_score` (float): Predicted volatility multiplier.
  - `volatility_forecast` (STABLE/ACCELERATING).

## Acceptance Criteria
- Successfully predict Gamma-induced "Flip Zones" (where market character changes) with 75% accuracy.
- Alert the Trader department within 10 seconds of price breaching a major Gamma support level.
