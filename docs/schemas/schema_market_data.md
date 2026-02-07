# Schema: Market Data

## File Location
`schemas/market_data.py`

## Purpose
Pydantic models for market data including real-time quotes, OHLCV bars, earnings calendars, and data source health monitoring.

---

## Models

### Quote
**Real-time stock quote.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `open` | `float` | `0.0` | Opening price | OHLC data |
| `high` | `float` | `0.0` | Day's high | OHLC data |
| `low` | `float` | `0.0` | Day's low | OHLC data |
| `price` | `float` | `0.0` | Current/last price | Primary display |
| `volume` | `int` | `0` | Trading volume | Volume analysis |
| `latest_trading_day` | `Optional[str]` | `None` | Most recent trading day | Date reference |
| `previous_close` | `float` | `0.0` | Prior day close | Change calculation |
| `change` | `float` | `0.0` | Price change | Display |
| `change_percent` | `str` | `"0.00%"` | Percentage change | Display |
| `timestamp` | `datetime` | `datetime.now()` | Quote timestamp | Freshness |
| `source` | `str` | `"alpha_vantage"` | Data provider | Attribution |

---

### OHLCV
**OHLCV candlestick bar.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `timestamp` | `datetime` | *required* | Bar timestamp | Time series |
| `open` | `float` | *required* | Open price | Charting |
| `high` | `float` | *required* | High price | Charting |
| `low` | `float` | *required* | Low price | Charting |
| `close` | `float` | *required* | Close price | Charting |
| `adjusted_close` | `Optional[float]` | `None` | Adjusted close | Analysis |
| `volume` | `int` | *required* | Volume | Volume analysis |
| `dividend` | `Optional[float]` | `None` | Dividend amount | Adjustment |
| `split_coefficient` | `Optional[float]` | `None` | Split ratio | Adjustment |

---

### Earnings
**Earnings calendar entry.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `name` | `Optional[str]` | `None` | Company name | Display |
| `report_date` | `str` | *required* | Expected report date | Scheduling |
| `fiscal_date_ending` | `Optional[str]` | `None` | Fiscal period end | Period reference |
| `estimate` | `Optional[float]` | `None` | EPS estimate | Expectations |
| `currency` | `str` | `"USD"` | Currency | Normalization |

---

### MarketDataHealth
**Health status of market data sources.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `source_name` | `str` | *required* | Data provider name | Identification |
| `status` | `str` | *required* | Connection status | Monitoring |
| `requests_remaining` | `dict` | *required* | API rate limits | Quota tracking |
| `overall_status` | `str` | *required* | Overall health | Dashboard |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `MarketDataService` | Quote retrieval |
| `HistoricalDataService` | OHLCV data |
| `EarningsService` | Calendar data |
| `HealthMonitoringService` | Source monitoring |
