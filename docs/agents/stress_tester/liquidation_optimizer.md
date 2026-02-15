# Liquidation Optimizer (Agent 16.3)

## ID: `liquidation_optimizer`

## Role & Objective
The 'Adversarial Feed'. Injects incorrect, delayed, or "Poisoned" market data into the ingestion pipeline to test the system's outlier detection and data-cleaning logic.

## Logic & Algorithm
- **Data Poisoning**: Mimics "Flash Crash" scenarios by injecting fake price-spikes or zero-liquidity data points.
- **Sanity Validation**: Checks if the Data Scientist or Trader identifies the bad data before acting on it.
- **Source Switching**: Simulates a "Primary Data Provider" failure to test the hot-swap speed to secondary feeds.

## Inputs & Outputs
- **Inputs**:
  - `clean_market_data` (Stream).
- **Outputs**:
  - `adversarial_market_feed` (Stream): The poisoned data delivered to the OS.

## Acceptance Criteria
- Trigger the system's "Data Integrity Alert" for 100% of injected outlier events.
- Ensure no "Adversarial" trade is triggered by fake price data.
