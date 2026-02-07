# Backend Service: Charting

## Overview
The **Charting Service** is the backbone of the platform's visual intelligence. It transforms raw financial time-series data into structured, multi-timeframe datasets optimized for high-performance rendering in the frontend. It supports professional-grade chart types, technical indicator overlays, and dynamic aggregation.

## Core Capabilities

### 1. Data Preparation Engine (`charting_service.py`)
Prepares OHLCV (Open, High, Low, Close, Volume) data for consumption by D3.js or Plotly charts.
- **Advanced Chart Types**:
    - **Standard**: Candlestick, Line, and Area charts.
    - **Quantitative**: **Heikin-Ashi** transformations for noise reduction and trend clarity.
- **Multi-Timeframe Support**: Dynamically resamples high-frequency data into 10 distinct timeframes ranging from **1-minute** (intraday) to **1-year** (macro) periods, ensuring correct OHLC aggregation at every level.

### 2. Analytical Overlays
The service orchestrates the calculation of technical studies ($indicators$) and maps them directly to the price timeline, enabling a unified view of market action and signal data.

### 3. Smart Persistence
To minimize the load on market data providers and ensure sub-second chart loading:
- **Tiered Caching**:
    - **Intraday Charts**: 5-minute cache TTL to maintain freshness.
    - **Daily+ Charts**: 1-hour cache TTL for stable historical data.

## Constants & Schema
- **Timeframes**: `1min`, `5min`, `15min`, `30min`, `1hr`, `4hr`, `1day`, `1week`, `1month`, `1year`.
- **Chart Types**: `CANDLESTICK`, `LINE`, `AREA`, `HEIKIN_ASHI`.

## Dependencies
- `pandas`: Powers the high-speed resampling and Heikin-Ashi mathematical transformations.
- `numpy`: Used for volatility and returns simulation in mock modes.
- `services.analysis.technical_analysis_service`: Provides the underlying math for indicators.
- `services.data.alpha_vantage`: The primary source for historical price bars.

## Usage Examples

### Fetching Daily Candlestick Data with Indicators
```python
from services.charting.charting_service import get_charting_service

chart_svc = get_charting_service()

# Get 1-day candlestick data for AAPL with SMA and RSI overlays
chart_data = await chart_svc.get_chart_data(
    symbol="AAPL",
    timeframe="1day",
    chart_type="candlestick",
    indicators=["SMA", "RSI"]
)

print(f"Retrieved {chart_data['metadata']['data_points']} data points.")
print(f"Indicators available: {list(chart_data['indicators'].keys())}")
```

### Aggregating 1-Minute Data to 15-Minute Bars
```python
import pandas as pd
from services.charting.charting_service import get_charting_service

chart_svc = get_charting_service()

# source_df contains 1-minute OHLCV data
fifteen_min_df = await chart_svc.aggregate_timeframe(
    data=source_df,
    source_timeframe="1min",
    target_timeframe="15min"
)
```
