# Delta Hedger (Agent 6.4)

## ID: `delta_hedger`

## Role & Objective
The "Risk Neutralizer". The Delta Hedger ensures the portfolio's directional risk is mathematically neutralized according to the specific safety tolerances of the Sovereign OS.

## Logic & Algorithm
1. **Exposure Summation**: Aggregates net delta (directional bias) from all assets (Stocks, Options, Futures).
2. **Neutralization Math**: Calculates the exact number of shares or futures needed to offset the current bias.
3. **Drift Enforcement**: Automatically triggers hedge adjustments whenever the net portfolio delta drifts more than 5% from its neutral target.

## Inputs & Outputs
- **Inputs**:
  - `position_deltas` (Dict): Delta breakdown by asset class.
  - `risk_policy` (Dict): Safety thresholds.
- **Outputs**:
  - `hedge_adjustment_qty` (int): Units required for re-neutralization.

## Acceptance Criteria
- Maintain a net portfolio delta within the ±5% safety band at all times.
- Hedge adjustments must be executed with a preference for liquidity-rich instruments (e.g., SPY or ES Futures).
