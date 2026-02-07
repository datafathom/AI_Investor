# Schema: FX Price

## File Location
`schemas/fx_price.py`

## Purpose
Pydantic model for foreign exchange currency pair pricing. Represents real-time FX tick data including bid/ask/mid prices for institutional FX trading simulation.

---

## Models

### FXPrice
**Currency pair tick data.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `pair` | `str` | *required* | Currency pair (e.g., `EURUSD`) | Identification |
| `bid` | `float` | *required, >0* | Bid price | Buy price |
| `ask` | `float` | *required, >0* | Ask price | Sell price |
| `mid` | `float` | *required, >0* | Mid-market price | Reference price |
| `timestamp` | `datetime` | `datetime.utcnow` | Tick timestamp | Time series |
| `source` | `str` | `"INSTITUTIONAL_SIM"` | Data source | Attribution |

**Validators:**
- `validate_mid`: Ensures mid price is between bid and ask (with tolerance for fast markets)

---

## Integration Points

| Service | Usage |
|---------|-------|
| `FXPricingService` | Real-time FX data |
| `InstitutionalTradingService` | FX execution |
| `CorrelationService` | Currency correlation analysis |
