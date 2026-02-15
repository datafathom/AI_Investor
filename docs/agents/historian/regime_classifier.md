# Regime Classifier (Agent 15.2)

## ID: `regime_classifier`

## Role & Objective
The 'Memory Keeper'. Captures high-level outcomes of inter-agent collaboration and market events to build a 'Lessons Learned' repository, helping the system recognize recurring financial "Regimes".

## Logic & Algorithm
- **Regime Labeling**: Tags historical time-blocks with descriptive labels: "Zero Interest Rate Euphoria," "Inflationary Burn," "Volatility Spike," etc.
- **Outcome Correlation**: Maps the performance of the Strategist's models to these specific regimes.
- **Feature Extraction**: Identifies the leading indicators that preceded a regime shift in the past.

## Inputs & Outputs
- **Inputs**:
  - `historical_market_data` (Data): Prices, yields, and macro stats.
  - `trading_pnl_history` (Data): Portfolio performance.
- **Outputs**:
  - `classified_memory_node` (Graph): A new node in the Neo4j "Institutional Memory" graph.

## Acceptance Criteria
- Correctly classify 90% of past market regimes defined in standard financial literature.
- Provide a "Similarity Score" for the current market state versus the best-matching historical regime.
