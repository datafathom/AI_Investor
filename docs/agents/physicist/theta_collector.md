# Theta Collector (Agent 6.1)

## ID: `theta_collector`

## Role & Objective
The "Time-Decay Harvester". The Theta Collector ensures the portfolio generates consistent income through the mathematical erosion of option value over time.

## Logic & Algorithm
1. **Decay Tracking**: Calculates dailyUSD impact of time-decay across all option holdings.
2. **Acceleration Detection**: Identifies positions entering the "Gamma/Theta Ramp" (last 30-45 days of life) where decay is most aggressive.
3. **Strategic Ingestion**: Recommends high-probability short-dated option sales (Covered Calls, Puts) to maintain target daily yields.

## Inputs & Outputs
- **Inputs**:
  - `option_positions` (List): Tickers, strikes, and expiries.
  - `target_daily_yield` (float): Minimum desired USD daily decay.
- **Outputs**:
  - `theta_snapshot` (float): Total portfolio theta.
  - `yield_projections` (Dict): Projected income for 7/30 day windows.

## Acceptance Criteria
- Maintain a portfolio-wide positive theta balance as defined by the risk policy.
- Provide yield projections accurate to within 2% of actual decay, assuming constant price.
