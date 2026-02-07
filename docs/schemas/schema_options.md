# Schema: Options

## File Location
`schemas/options.py`

## Purpose
Pydantic models for options trading including option legs, multi-leg strategies, Greeks calculations, and P&L analysis.

---

## Enums

### OptionType
**Option contract type.**

| Value | Description |
|-------|-------------|
| `CALL` | Right to buy |
| `PUT` | Right to sell |

---

### OptionAction
**Trade action.**

| Value | Description |
|-------|-------------|
| `BUY` | Buy to open |
| `SELL` | Sell to open |

---

## Models

### OptionLeg
**Single leg of an options strategy.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `symbol` | `str` | *required* | Underlying symbol | Identification |
| `option_type` | `OptionType` | *required* | Call or put | Contract type |
| `action` | `OptionAction` | *required* | Buy or sell | Position direction |
| `strike` | `float` | *required* | Strike price | Contract spec |
| `expiration` | `datetime` | *required* | Expiration date | Contract spec |
| `quantity` | `int` | *required* | Number of contracts | Position size |
| `premium` | `float` | *required* | Option premium | Price |

---

### OptionsStrategy
**Multi-leg options strategy.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy identifier | Primary key |
| `strategy_name` | `str` | *required* | Name: `iron_condor`, `butterfly`, etc. | Classification |
| `legs` | `List[OptionLeg]` | *required* | Strategy legs | Structure |
| `underlying_symbol` | `str` | *required* | Underlying stock | Identification |
| `max_profit` | `float` | *required* | Maximum profit | Risk/reward |
| `max_loss` | `float` | *required* | Maximum loss | Risk/reward |
| `breakeven_points` | `List[float]` | *required* | Breakeven prices | Analysis |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |

---

### Greeks
**Option Greeks for a single position.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `delta` | `float` | *required* | Price sensitivity | Hedging |
| `gamma` | `float` | *required* | Delta sensitivity | Second-order risk |
| `theta` | `float` | *required* | Time decay | Daily decay |
| `vega` | `float` | *required* | Volatility sensitivity | Vol risk |
| `rho` | `float` | *required* | Rate sensitivity | Rate risk |

---

### StrategyGreeks
**Aggregated Greeks for entire strategy.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy reference | Linking |
| `net_delta` | `float` | *required* | Total delta | Direction risk |
| `net_gamma` | `float` | *required* | Total gamma | Convexity risk |
| `net_theta` | `float` | *required* | Total theta | Daily P&L |
| `net_vega` | `float` | *required* | Total vega | Vol exposure |
| `calculated_date` | `datetime` | *required* | Calculation time | Freshness |

---

### StrategyPnL
**Strategy profit/loss at various prices.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy reference | Linking |
| `underlying_prices` | `List[float]` | *required* | Price scenarios | X-axis |
| `pnl_values` | `List[float]` | *required* | P&L at each price | Y-axis |
| `expiration_pnl` | `List[float]` | *required* | P&L at expiration | Terminal value |

---

### StrategyAnalysis
**Complete strategy analysis.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy reference | Linking |
| `greeks` | `StrategyGreeks` | *required* | Strategy Greeks | Risk metrics |
| `pnl` | `StrategyPnL` | *required* | P&L analysis | Payoff analysis |
| `probability_of_profit` | `float` | *required* | Win probability | Risk assessment |
| `expected_value` | `float` | *required* | Expected P&L | Expectancy |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `OptionsService` | Options data and execution |
| `GreeksCalculationService` | Greeks computation |
| `OptionsAnalysisService` | Strategy analysis |

## Frontend Components
- Options dashboard (FrontendOptions)
- Strategy builder
- P&L diagram
- Greeks display
