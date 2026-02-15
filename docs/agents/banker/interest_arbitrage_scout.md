# Interest Arbitrage Scout (Agent 18.6)

## ID: `interest_arbitrage_scout`

## Role & Objective
The 'Yield Hunter'. Identifies the best risk-adjusted return on swap-liquidity versus idle cash in bank accounts, moving capital where it earns the highest "Passive Alpha".

## Logic & Algorithm
- **Venue Sourcing**: Scans APY/APR for institutional savings (TradFi) and lending protocols (DeFi).
- **Transfer Cost Analysis**: Calculates gas fees, bank fees, and slippage to ensure the "Transfer" is net-profitable.
- **Hot-Swap Execution**: Issues movement commands to the ache_wire_tracker or DeFi integration services.

## Inputs & Outputs
- **Inputs**:
  - `market_yield_landscape` (Data).
- **Outputs**:
  - `yield_optimization_plan` (Dict): Recommended movements.

## Acceptance Criteria
- Identify a +50bps yield delta within 10 minutes of market updates.
- Ensure all "Arbitrage Move" transactions are net-positive after all friction costs.
