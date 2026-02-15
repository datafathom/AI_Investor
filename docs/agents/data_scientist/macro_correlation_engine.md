# Macro Correlation Engine (Agent 3.6)

## ID: `macro_correlation_engine`

## Role & Objective
The 'Big Picture' analyst. Connects macro-economic indicators (Rate Hikes, Employment) to sector-specific price movement.

## Logic & Algorithm
- Ingests Federal Reserve API data and global macro calendars.
- Maps sensitivity (Beta) of the user's portfolio to macro shocks.
- Simulates 'Recession' and 'Hyperinflation' scenarios.

## Inputs & Outputs
- **Inputs**:
  - `portfolio_snapshot` (Dict): Breakdown of current holdings.
  - `macro_shocks` (List): Simulated events (e.g., '+50bps hike').
- **Outputs**:
  - `resilience_score` (float): Expected portfolio impact in USD.
  - `hedging_recommendations (List): Assets meant to offset macro risk.

## Acceptance Criteria
- Simulate 10 macro scenarios across the entire portfolio in under 3 seconds.
- Achieve 90% correlation between simulated shocks and historical market reactions to similar events.
