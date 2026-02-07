# Backend Service: Data

## Overview
The **Data Service** is the platform's high-fidelity ingestion and normalization hub. It aggregates raw financial data from over a dozen external providers (Alpha Vantage, FRED, Polygon, Google Trends, etc.) and fuses them into a unified mathematical "Market State Tensor." This ensures that both human users and AI agents have a consistent, normalized view of market volatility, sentiment, and macroeconomic health.

## Core Components

### 1. Data Fusion Engine (`data_fusion_service.py`)
The primary orchestrator for cross-domain data normalization.
- **Market State Tensor**: Fuses Price Momentum, Retail Sentiment, Options Flow (Smart Money), and Macro Health into a 0.0–1.0 scaled tensor.
- **Validation & Quarantine**: Implements data integrity checks (staleness, impossible values) and "quarantines" suspicious data to prevent AI agents from acting on corrupted signals.
- **Sigmoid Normalization**: Uses mathematical sigmoid functions to map disparate metrics (like Z-scores or basis points) into a consistent range.

### 2. External Data Providers
- **Equity Intelligence (`alpha_vantage.py`, `polygon_service.py`)**: Fetches real-time quotes, historical OHLCV bars, and institutional earnings calendars. Features robust rate-limiting via the `APIGovernor`.
- **Macroeconomic Engine (`fred_service.py`)**: Monitors the Federal Reserve's economic data (Yield Curve, CPI, Unemployment). 
    - **Regime Analysis**: Automatically classifies the economic state into categories like `EXPANSION`, `SLOWDOWN`, or `RECESSION_WARNING`.
- **Sentiment & Alternatives (`google_trends.py`, `reddit_service.py`)**: Ingests retail interest and social volume to quantify "herd behavior" and market fear/greed.

### 3. Options & Flow (`options_service.py`)
- **Smart Money Tracking**: Monitors Put/Call ratios and whale movement in the options market to identify directional bias before it reflects in spot prices.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Market Terminal** | Advanced Charts (OHLCV) | `alpha_vantage.get_intraday()` |
| **Market Terminal** | Sentiment Meter | `google_trends.get_trend_score()` |
| **Macro Dashboard** | Yield Curve Visualizer | `fred_service.get_yield_curve_data()` |
| **Macro Dashboard** | Regime Pulse | `fred_service.get_macro_regime()` |
| **AI Strategy Hub** | Tensor Heatmap | `data_fusion_service.get_market_state_tensor()` |
| **Earnings Center** | Calendar Timeline | `alpha_vantage.get_earnings_calendar()` |

## Dependencies
- `httpx`: High-performance asynchronous HTTP client for parallel API fetching.
- `numpy`: Used for multi-dimensional tensor calculations and normalization.
- `pydantic`: Enforces schemas for `Quote`, `OHLCV`, `MacroRegime`, and `Earnings`.
- `services.system.api_governance`: Manages API keys and tier-based rate limits.

## Usage Examples

### Generating a Market State Tensor for TSLA
```python
from services.data.data_fusion_service import DataFusionService

fusion = DataFusionService()

# Generates a normalized 0-1 set of metrics
state = fusion.get_market_state_tensor(symbol="TSLA")

print(f"Aggregate Market Score: {state['aggregate_score']}")
print(f"Retail Sentiment: {state['tensor']['retail_sentiment']}")
```

### Fetching Economic Regime from FRED
```python
from services.data.fred_service import get_fred_service

fred = get_fred_service()

regime = await fred.get_macro_regime()
print(f"Economic Status: {regime.status}")
print(f"Health Score: {regime.health_score}/100")
```
