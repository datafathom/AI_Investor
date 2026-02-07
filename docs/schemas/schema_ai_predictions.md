# Schema: AI Predictions

## File Location
`schemas/ai_predictions.py`

## Purpose
Pydantic models for AI-driven price predictions, market regime detection, trend analysis, and sentiment scoring. Supports the platform's predictive analytics features including price forecasting, trend identification, and market condition assessment.

---

## Enums

### PredictionType
**Types of predictions the system can generate.**

| Value | Description |
|-------|-------------|
| `PRICE` | Direct price point predictions |
| `TREND` | Directional trend predictions (up/down/sideways) |
| `VOLATILITY` | Volatility forecasts |
| `MARKET_REGIME` | Broad market condition detection |

---

## Models

### PricePrediction
**A specific price prediction for a security.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `prediction_id` | `str` | *required* | Unique prediction identifier | Tracking, backtesting, performance analysis |
| `symbol` | `str` | *required* | Stock/asset ticker symbol | Security identification |
| `predicted_price` | `float` | *required* | Predicted price target | Display, trading signal generation |
| `confidence` | `float` | *required, 0-1* | Model confidence in prediction | Filter low-confidence predictions, risk weighting |
| `prediction_date` | `datetime` | *required* | When prediction was generated | Validity window, model versioning |
| `time_horizon` | `str` | *required* | Forecast period: `1d`, `1w`, `1m`, `3m`, `1y` | Matching predictions to investment horizons |
| `confidence_interval` | `Dict[str, float]` | `{}` | Lower/upper bounds: `{lower: value, upper: value}` | Range-based trading, risk assessment |
| `model_version` | `str` | *required* | ML model version that generated this | Model comparison, A/B testing, rollback capability |

---

### TrendPrediction
**Directional trend forecast for a security.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `prediction_id` | `str` | *required* | Unique prediction identifier | Tracking and analysis |
| `symbol` | `str` | *required* | Stock/asset ticker symbol | Security identification |
| `trend_direction` | `str` | *required* | Predicted direction: `bullish`, `bearish`, `neutral` | Signal generation, portfolio tilting |
| `trend_strength` | `float` | *required, 0-1* | How strong the predicted trend is | Weighting in multi-signal strategies |
| `predicted_change` | `float` | *required* | Expected percentage price change | Position sizing, target setting |
| `time_horizon` | `str` | *required* | Forecast period | Matching to holding periods |
| `confidence` | `float` | *required* | Model confidence score | Filtering and ranking |

---

### MarketRegime
**Detected market regime/condition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `regime_id` | `str` | *required* | Unique regime detection ID | Historical tracking |
| `regime_type` | `str` | *required* | Market state: `bull`, `bear`, `sideways`, `volatile` | Strategy selection, risk adjustment |
| `confidence` | `float` | *required* | Detection confidence | Threshold-based regime confirmation |
| `detected_date` | `datetime` | *required* | When regime was detected | Regime duration tracking |
| `expected_duration` | `Optional[str]` | `None` | Predicted regime duration | Planning horizon adjustment |

**Property:** `regime` - Alias for `regime_type` for test compatibility.

---

### SentimentAnalysisResult
**Aggregated sentiment analysis output.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `symbol` | `Optional[str]` | `None` | Associated ticker (None for market-wide) | Security-specific vs. market sentiment |
| `overall_sentiment` | `float` | *required* | Net sentiment score | Primary sentiment indicator |
| `positive_score` | `float` | *required* | Proportion of positive signals | Sentiment composition analysis |
| `negative_score` | `float` | *required* | Proportion of negative signals | Contrarian signal detection |
| `neutral_score` | `float` | `0.0` | Proportion of neutral signals | Market attention gauge |
| `sentiment_label` | `str` | `"neutral"` | Human-readable label | UI display |
| `confidence` | `float` | `0.0` | Analysis confidence | Quality filtering |
| `analysis_date` | `datetime` | `datetime.utcnow` | When analysis was performed | Freshness check |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `PredictionEngine` | Generates all prediction types |
| `AIAnalyticsService` | Market regime and trend analysis |
| `SentimentAnalysisService` | News and social sentiment scoring |
| `TradingStrategyService` | Consumes predictions for signal generation |

## API Endpoints
- `GET /api/predictions/price/{symbol}` - Get price predictions for a symbol
- `GET /api/predictions/trend/{symbol}` - Get trend analysis
- `GET /api/predictions/regime` - Get current market regime
- `GET /api/predictions/sentiment` - Get sentiment analysis

## Frontend Components
- Prediction dashboard (FrontendAI)
- Price target visualization
- Market regime indicator
- Sentiment gauge widgets
