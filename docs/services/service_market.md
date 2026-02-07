# Backend Service: Market (Tactical Intelligence)

## Overview
The **Market Service** is the platform's core tactical data and sentiment infrastructure. It processes high-frequency "Market Bytes," normalizing heterogeneous Level 2 order depth from multiple liquidity providers into a consistent internal format. Beyond raw data, the service provides advanced quantitative metrics such as **VWAP-for-Size** (execution price estimation), **Orderflow Toxicity (VPIN)** for liquidity crash prediction, and a composite **Fear & Greed Index** to gauge macro-sentiment regimes.

## Core Components

### 1. Level 2 Orderbook Parser (`level2_parser.py`)
The system's high-fidelity data bridge.
- **Normalization Engine**: Transforms raw depth payloads from disparate providers into a standardized snapshot featuring sorted Bids/Asks, mid-prices, and spread calculations. It ensures that all tactical agents operate on a unified view of the market's limit order book.

### 2. Liquidity Aggregator (`depth_aggregator.py`)
Computes execution-quality and depth metrics.
- **VWAP-for-Size**: Estimates the actual fill price for a specific order size by traversing the order book levels (essential for non-slippage trading).
- **Volume Imbalance**: Calculates the net volume bias within a specific price range (e.g., ±5 pips) to detect hidden selling pressure or "Bid Walls."

### 3. Fear & Greed Sentiment Service (`fear_greed_service.py`)
The platform's psychological barometer.
- **Composite Sentiment**: Merges VIX (Volatility) contribution with momentum proxies to generate a score from 0-100 (Extreme Fear to Extreme Greed).
- **Regime Classification**: Categorizes the market into sentiment buckets, allowing risk-management agents to proactively adjust exposure based on the prevailing psychological regime.

### 4. Toxicity Monitor (`toxicity_monitor.py`)
Detects impending liquidity crises via Orderflow Toxicity.
- **VPIN (Volume-synchronized Probability of Informed Trading)**: Measures the imbalance between buy/sell volume relative to total volume. Significant spikes in VPIN ("Toxicity Alerts") indicate that informed traders may be overwhelming market markers, signaling an impending liquidity vacuum or price crash.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Real-Time Depth Visualizer | `level2_parser.parse_depth_event()` |
| **Trading Terminal** | Slippage Estimator (VWAP) | `depth_aggregator.get_vwap_for_size()` |
| **Market Intelligence** | Fear & Greed Dial | `fear_greed_service.get_latest()` |
| **System Monitor** | Liquidity Toxicity Alert | `toxicity_monitor.calculate_vpin_status()` |
| **Portfolio Detail** | Sentiment Component Table | `fear_greed_service.calculate_score()` |

## Dependencies
- `math / random`: Generates sentiment simulations and composite weightings.
- `datetime`: Provides micro-second precision for high-frequency pricing data.
- `logging`: Records structural events like "Significant Liquidity Imbalance" or "Extreme Toxicity Detected."

## Usage Examples

### Normalizing a Raw Level 2 Depth Event
```python
from services.market.level2_parser import Level2Parser

parser = Level2Parser()

# Raw feed from a liquidity provider
raw_msg = {
    "symbol": "BTC/USD",
    "timestamp": "2026-02-06T23:55:00Z",
    "bids": [{"price": 42000.50, "size": 1.5}, {"price": 41999.00, "size": 10}],
    "asks": [{"price": 42001.00, "size": 2.1}, {"price": 42002.50, "size": 5.0}]
}

book = parser.parse_depth_event(payload=raw_msg)
print(f"Mid: {book['mid']} | Spread: {book['spread']} | Depth: {book['depth_levels']} levels")
```

### Estimating Fill Price (VWAP) for a Large SELL Order
```python
from services.market.depth_aggregator import DepthAggregator

aggregator = DepthAggregator()

# book comes from parser...
size_to_sell = 10.0
vwap = aggregator.get_vwap_for_size(book=book, size=size_to_sell, direction="SELL")

print(f"Projected Fill Price for {size_to_sell} units: ${vwap:,.2f}")
```

### Checking for Orderflow Toxicity
```python
from services.market.toxicity_monitor import ToxicityMonitor

monitor = ToxicityMonitor()

# Input: 500 Buy units, 2500 Sell units in a single volume bucket
status = monitor.calculate_vpin_status(buy_volume=500, sell_volume=2500, avg_vpin=0.20)

if status['toxicity_alert']:
    print(f"TOXICITY ALERT! Score: {status['vpin_score']} | Risk: {status['liquidity_risk']}")
```
