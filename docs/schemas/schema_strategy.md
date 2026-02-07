# Schema: Strategy

## File Location
`schemas/strategy.py`

## Purpose
Pydantic models for investment strategies including strategy definitions, signal generation, backtesting, and strategy performance tracking.

---

## Models

### Strategy
**Investment strategy definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy identifier | Primary key |
| `user_id` | `str` | *required* | Strategy creator | Attribution |
| `strategy_name` | `str` | *required* | Display name | Identification |
| `strategy_type` | `str` | *required* | Type: `momentum`, `value`, `mean_reversion`, `ml` | Classification |
| `description` | `str` | *required* | Strategy description | Documentation |
| `parameters` | `Dict` | `{}` | Strategy parameters | Configuration |
| `universe` | `List[str]` | `[]` | Stock universe | Scope |
| `is_active` | `bool` | `True` | Whether active | Status |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last update | Freshness |

---

### StrategySignal
**Trading signal from strategy.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `signal_id` | `str` | *required* | Signal identifier | Primary key |
| `strategy_id` | `str` | *required* | Source strategy | Linking |
| `symbol` | `str` | *required* | Stock ticker | Target |
| `signal_type` | `str` | *required* | Type: `buy`, `sell`, `hold` | Action |
| `strength` | `float` | *required, 0-1* | Signal strength | Confidence |
| `price_target` | `Optional[float]` | `None` | Target price | Execution |
| `stop_loss` | `Optional[float]` | `None` | Stop loss price | Risk |
| `signal_date` | `datetime` | *required* | Signal timestamp | Timing |
| `expiration_date` | `Optional[datetime]` | `None` | Signal expiration | Validity |

---

### StrategyBacktest
**Strategy backtest results.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `backtest_id` | `str` | *required* | Backtest identifier | Primary key |
| `strategy_id` | `str` | *required* | Tested strategy | Linking |
| `start_date` | `datetime` | *required* | Backtest start | Period |
| `end_date` | `datetime` | *required* | Backtest end | Period |
| `initial_capital` | `float` | *required* | Starting capital | Baseline |
| `final_value` | `float` | *required* | Ending value | Result |
| `total_return` | `float` | *required* | Total return | Performance |
| `cagr` | `float` | *required* | Compound annual return | Performance |
| `sharpe_ratio` | `float` | *required* | Risk-adjusted return | Quality |
| `max_drawdown` | `float` | *required* | Maximum drawdown | Risk |
| `win_rate` | `float` | *required* | Winning trade percentage | Quality |
| `trades` | `int` | *required* | Total trades | Activity |

---

### StrategyPerformance
**Live strategy performance metrics.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy identifier | Linking |
| `live_return` | `float` | *required* | Live return since activation | Performance |
| `signals_generated` | `int` | *required* | Total signals | Activity |
| `signals_executed` | `int` | *required* | Executed signals | Execution |
| `accuracy` | `float` | *required* | Signal accuracy | Quality |
| `last_signal_date` | `Optional[datetime]` | `None` | Most recent signal | Activity |
| `updated_date` | `datetime` | *required* | Last update | Freshness |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `StrategyService` | Strategy management |
| `SignalGenerationService` | Signal creation |
| `BacktestingService` | Historical testing |

## Frontend Components
- Strategy dashboard (FrontendStrategy)
- Strategy builder
- Backtest results
- Signal alerts
