# Backend Service: AI Predictions

## Overview
The **AI Predictions Service** is the quantitative forecasting arm of the AI Investor platform. It provides advanced analytics to detect market regimes, analyze the sentiment impact of news, and generate high-fidelity price and trend forecasts across various time horizons.

## Core Components

### AI Analytics Service (`ai_analytics_service.py`)
Provides high-level qualitative and contextual market analysis.
- **Role**: Combines news sentiment with price data to detect secondary effects and market cycles.
- **Key Features**:
    - **Sentiment Analysis**: Evaluates raw text to produce structured sentiment scores (Positive/Negative/Neutral).
    - **Market Regime Detection**: Classifies the overall market state (e.g., Bull, Bear, Sideways) and calculates detection confidence.
    - **News Impact Prediction**: Calculates the expected price change (%) and volatility impact driven by specific news events or social trends.

### Prediction Engine (`prediction_engine.py`)
The quantitative core responsible for numerical forecasting.
- **Role**: Uses historical data and ML models to project future asset performance.
- **Key Features**:
    - **Price Forecasting**: Predicts future price points for specific symbols across horizons (1d, 1w, 1m, 3m, 1y).
    - **Confidence Intervals**: Calculates lower and upper bounds for predictions based on historical volatility and model uncertainty.
    - **Trend Prediction**: Determines the overal direction (Bullish/Bearish) and strength of a price movement without necessarily predicting an exact price.
    - **Caching Layer**: Integrates with the system cache to serve repeated prediction requests instantly while maintaining freshness via TTL.

## Dependencies
- `numpy`: Used for numerical operations and interval calculations.
- `services.system.cache_service`: For result persistence and low-latency retrieval.
- `schemas.ai_predictions`: Defines models for `PricePrediction`, `TrendPrediction`, and `MarketRegime`.

## Usage Example

### Predicting Asset Price
```python
from services.ai_predictions.prediction_engine import get_prediction_engine

engine = get_prediction_engine()
pred = await engine.predict_price(symbol="AAPL", time_horizon="1m")
print(f"Predicted AAPL Price: ${pred.predicted_price:.2f}")
print(f"Range: ${pred.confidence_interval['lower']:.2f} - ${pred.confidence_interval['upper']:.2f}")
```

### Detecting Market Regime
```python
from services.ai_predictions.ai_analytics_service import get_ai_analytics_service

analytics = get_ai_analytics_service()
regime = await analytics.detect_market_regime(market_index="SPY")
print(f"Current Regime: {regime.regime_type} ({regime.confidence*100}% Confidence)")
```
