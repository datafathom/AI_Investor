# Schema: Index Fund

## File Location
`schemas/index_fund.py`

## Purpose
Pydantic models for index funds and ETFs. Captures fund characteristics including expense ratios, asset class focus, and tradability for passive investment screening and analysis.

---

## Models

### IndexFundBase
**Base model for index fund data.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `ticker` | `str` | *required* | Fund ticker symbol | Identification |
| `name` | `str` | *required* | Fund name | Display |
| `fund_type` | `str` | `"ETF"` | Type: `ETF`, `MUTUAL_FUND`, `INDEX` | Classification |
| `benchmark_index` | `Optional[str]` | `None` | Tracked index (e.g., S&P 500) | Tracking reference |
| `expense_ratio` | `float` | *required* | Annual expense ratio | Cost comparison |
| `aum` | `Optional[float]` | `0.0` | Assets under management | Size/liquidity |
| `inception_date` | `Optional[date]` | `None` | Fund launch date | Track record |
| `issuer` | `Optional[str]` | `None` | Fund provider (e.g., Vanguard) | Provider filtering |
| `asset_class` | `Optional[str]` | `"EQUITY"` | Asset class: `EQUITY`, `FIXED_INCOME`, `COMMODITY` | Classification |
| `sector_focus` | `Optional[str]` | `"BROAD_MARKET"` | Sector focus | Strategy filtering |
| `market_cap_focus` | `Optional[str]` | `"LARGE_CAP"` | Size focus: `LARGE_CAP`, `MID_CAP`, `SMALL_CAP` | Size filtering |
| `geography` | `Optional[str]` | `"US"` | Geographic focus | Region filtering |
| `tradability` | `Optional[str]` | `"HIGHLY_LIQUID"` | Liquidity level | Trading suitability |

---

### IndexFund
**Full index fund record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `is_active` | `bool` | `True` | Whether fund is active | Filtering |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |
| `updated_at` | `datetime` | `datetime.now()` | Last update | Freshness |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `IndexFundService` | Fund data management |
| `ScreeningService` | Fund screening |
| `PortfolioConstructionService` | Passive allocation |
