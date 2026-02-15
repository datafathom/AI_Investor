# Correlation Detective (Agent 3.3)

## ID: `correlation_detective`

## Role & Objective
Statistical relationship analyzer. Identifies lead/lag patterns between disparate assets (e.g., BTC vs Nikkei).

## Logic & Algorithm
- Runs Pearson/Spearman correlation matrices across asset clusters.
- Identifies regime-specific decoupling events.
- Flags high-confidence 'Pair Trading' opportunities.

## Inputs & Outputs
- **Inputs**:
  - `asset_pair` (Tuple): Tickers to compare.
  - `lookback_period` (int): Number of days for the analysis.
- **Outputs**:
  - `correlation_coefficient` (float): Strength of the relationship.
  - `divergence_alert` (bool): True if historical correlation has broken.

## Acceptance Criteria
- Analysis of a 10-asset matrix must complete in under 1 second.
- Divergence alerts must be issued within 1 minute of a significant correlation break.
