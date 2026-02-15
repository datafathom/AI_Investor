# Exit Manager (Agent 5.2)

## ID: `exit_manager`

## Role & Objective
The "Profit Protector". The Exit Manager manages the lifecycle of an open position to ensure profits are realized according to the plan and losses are strictly capped.

## Logic & Algorithm
1. **Dynamic Vol-Stops**: Manages trailing stops based on real-time ATR (Average True Range).
2. **Time-Exit Enforcement**: Closes out short-term tactical positions before market sessions close to avoid overnight risk.
3. **Scaling Strategy**: Gradually reduces position size as the asset approaches the target take-profit level.

## Inputs & Outputs
- **Inputs**:
  - `open_positions` (List): Current portfolio holdings.
  - `volatility_metrics` (Dict): Current market ATR.
- **Outputs**:
  - `exit_orders` (List): Orders to trim or close positions.

## Acceptance Criteria
- 100% of open positions must have an active, server-side stop-loss order within 1 second of entry.
- Trailing stops must be updated in real-time as the asset price moves in favor of the trade.
