# Documentation: `tests/integration/test_data_ingestion.py`

## Overview
This integration test validates "Phase 6: The Data Tap". It ensures that market data can be successfully fetched from external providers (Alpha Vantage) and published to the internal messaging backbone (Kafka).

## Components Under Test
- `services.data.alpha_vantage.AlphaVantageClient`: For fetching external price data.
- `services.data.producer.MarketDataProducer`: For publishing data to Kafka topics.

## Test Workflow

### `run_test_ingestion`
1. **API Fetch**: Attempts to get the latest quote for a symbol (default "SPY").
2. **Mock Fallback**: If no API key is present in the environment, the test automatically falls back to static mock data to allow the rest of the pipeline to be verified.
3. **Kafka Publication**: Connects to the `MarketDataProducer` and attempts to publish the quote to the `market.equity` topic.

## Success Criteria
- Successful API response or mock data generation.
- Existence of an active Kafka producer.
- Successful message dispatch to the relevant Kafka topic.

## Holistic Context
This test verifies the "Inhale" part of the platform. If this integration fails, the system is effectively blind and paralyzed, having no market information to process or trade upon.
