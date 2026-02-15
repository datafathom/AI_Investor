# Anomaly Scout (Agent 3.4)

## ID: `anomaly_scout`

## Role & Objective
Outlier detection specialist. Monitors live data streams for 'impossible' price action or volume spikes.

## Logic & Algorithm
- Applies Z-score analysis to incoming price/volume events.
- Isolates 'Flash Crashes' from organic volatility.
- Correlates anomalies with news events via the Scraper General.

## Inputs & Outputs
- **Inputs**:
  - `live_stream_item` (Dict): Recent ticker price/volume data.
- **Outputs**:
  - `anomaly_score` (float): Probability that the event is an outlier.
  - `shock_type` (str): Categorization (e.g., 'FAT_FINGER', 'WHALE_EXIT').

## Acceptance Criteria
- Detect anomalies in the market ticker within 50ms of event ingestion.
- Maintain a false-positive rate < 5% during high-volatility regimes.
