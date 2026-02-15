# Asset Hunter (Agent 7.6)

## ID: `asset_hunter`

## Role & Objective
The 'Opportunity Scout'. The bridge between Hunter and Data Scientist. Synthesizes all Hunter inputs into a find/buy signal for growth-stage assets.

## Logic & Algorithm
- Correlates Whitepaper scores with Deal Flow rankings.
- Proposes new 'Growth' sector investments to the Orchestrator.
- Monitors 'Under-The-Radar' assets before they hit mainstream exchanges.

## Inputs & Outputs
- **Inputs**:
  - `all_funnel_results` (List): Aggregated data from agents 7.1 - 7.5.
- **Outputs**:
  - `buy_signal` (Dict): Ticker, Reason, and Recommended Alpha Allocation.

## Acceptance Criteria
- Consolidate input from 5 Hunter agents into a single "Alpha Signal" in < 2 seconds.
- Achieve a 70% correlation between high-ranked signals and subsequent 3-month asset performance.
