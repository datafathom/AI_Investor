# Schema: Paper Trading

## File Location
`schemas/paper_trading.py`

## Purpose
Pydantic models for paper trading simulation including virtual orders, portfolios, and backtesting results without real money at risk.

---

## Models

### PaperOrder
**Simulated paper trade order.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `order_id` | `str` | *required* | Unique order ID | Primary key |
| `user_id` | `str` | *required* | Trader | Attribution |
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `side` | `str` | *required* | Side: `buy`, `sell` | Direction |
| `order_type` | `str` | *required* | Type: `market`, `limit` | Order type |
| `quantity` | `int` | *required* | Share quantity | Size |
| `limit_price` | `Optional[float]` | `None` | Limit price | Price constraint |
| `fill_price` | `Optional[float]` | `None` | Execution price | Result |
| `status` | `str` | `"pending"` | Order status | Lifecycle |
| `created_date` | `datetime` | *required* | Order creation | Timing |
| `filled_date` | `Optional[datetime]` | `None` | Execution time | Timing |

---

### VirtualPortfolio
**Simulated paper trading portfolio.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `portfolio_id` | `str` | *required* | Portfolio identifier | Primary key |
| `user_id` | `str` | *required* | Owner | Attribution |
| `portfolio_name` | `str` | *required* | Display name | Identification |
| `initial_cash` | `float` | *required* | Starting capital | Baseline |
| `current_cash` | `float` | *required* | Available cash | Buying power |
| `positions` | `Dict[str, Dict]` | `{}` | Holdings: `{symbol: {quantity, avg_cost}}` | Portfolio |
| `total_value` | `float` | *required* | Portfolio value | Performance |
| `pnl` | `float` | `0.0` | Profit/loss | Performance |
| `pnl_percentage` | `float` | `0.0` | Return percentage | Performance |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last update | Freshness |

---

### SimulationResult
**Backtesting simulation results.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `simulation_id` | `str` | *required* | Unique simulation ID | Primary key |
| `portfolio_id` | `str` | *required* | Portfolio used | Linking |
| `start_date` | `datetime` | *required* | Simulation start | Period |
| `end_date` | `datetime` | *required* | Simulation end | Period |
| `initial_value` | `float` | *required* | Starting value | Baseline |
| `final_value` | `float` | *required* | Ending value | Result |
| `total_return` | `float` | *required* | Total return | Performance |
| `sharpe_ratio` | `float` | *required* | Risk-adjusted return | Quality |
| `max_drawdown` | `float` | *required* | Largest drawdown | Risk |
| `win_rate` | `float` | *required* | Winning trade percentage | Accuracy |
| `trades` | `List[Dict]` | `[]` | Trade history | Analysis |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `PaperTradingService` | Simulation engine |
| `BacktestingService` | Historical backtests |
| `VirtualPortfolioService` | Portfolio management |

## Frontend Components
- Paper trading dashboard (FrontendPaperTrading)
- Virtual portfolio view
- Simulation results charts
