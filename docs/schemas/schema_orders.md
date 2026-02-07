# Schema: Orders

## File Location
`schemas/orders.py`

## Purpose
Pydantic models for advanced order types including trailing stops, bracket orders, conditional orders, and execution strategies for algorithmic trading.

---

## Enums

### OrderType
**Advanced order types.**

| Value | Description |
|-------|-------------|
| `MARKET` | Market order |
| `LIMIT` | Limit order |
| `STOP` | Stop order |
| `STOP_LIMIT` | Stop-limit order |
| `TRAILING_STOP` | Trailing stop order |
| `BRACKET` | Bracket order (OCO) |

---

### OrderStatus
**Order lifecycle status.**

| Value | Description |
|-------|-------------|
| `PENDING` | Awaiting submission |
| `SUBMITTED` | Sent to exchange |
| `PARTIAL` | Partially filled |
| `FILLED` | Completely filled |
| `CANCELLED` | Cancelled |
| `REJECTED` | Rejected by exchange |

---

## Models

### TrailingStopOrder
**Trailing stop order configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `order_id` | `str` | *required* | Unique order ID | Primary key |
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `quantity` | `int` | *required* | Share quantity | Size |
| `trail_amount` | `Optional[float]` | `None` | Dollar trail amount | Trail config |
| `trail_percent` | `Optional[float]` | `None` | Percentage trail | Trail config |
| `trigger_price` | `Optional[float]` | `None` | Current trigger | Dynamic tracking |
| `status` | `OrderStatus` | `PENDING` | Order status | Lifecycle |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |

---

### BracketOrder
**Bracket order with profit target and stop loss.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `order_id` | `str` | *required* | Unique order ID | Primary key |
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `entry_type` | `str` | *required* | Entry order type | Entry method |
| `entry_price` | `float` | *required* | Entry price | Entry |
| `quantity` | `int` | *required* | Share quantity | Size |
| `take_profit_price` | `float` | *required* | Profit target | Exit |
| `stop_loss_price` | `float` | *required* | Stop loss | Risk management |
| `status` | `OrderStatus` | `PENDING` | Order status | Lifecycle |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |

---

### ConditionalOrder
**Order triggered by market conditions.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `order_id` | `str` | *required* | Unique order ID | Primary key |
| `condition_type` | `str` | *required* | Trigger type: `price`, `volume`, `time` | Condition |
| `condition_value` | `float` | *required* | Trigger value | Threshold |
| `comparison` | `str` | *required* | Operator: `above`, `below`, `equals` | Comparison |
| `triggered_order` | `Dict` | *required* | Order to execute | Child order |
| `is_triggered` | `bool` | `False` | Whether triggered | State |

---

### ExecutionStrategy
**Algorithmic execution strategy.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `strategy_id` | `str` | *required* | Strategy identifier | Primary key |
| `strategy_type` | `str` | *required* | Type: `TWAP`, `VWAP`, `ICEBERG` | Algorithm |
| `total_quantity` | `int` | *required* | Total shares to execute | Target |
| `time_horizon` | `str` | *required* | Execution window | Duration |
| `slice_size` | `Optional[int]` | `None` | Individual order size | Slicing |
| `urgency` | `str` | `"normal"` | Urgency level | Aggressiveness |

---

### ExecutionResult
**Execution outcome.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `execution_id` | `str` | *required* | Execution identifier | Primary key |
| `strategy_id` | `str` | *required* | Parent strategy | Linking |
| `filled_quantity` | `int` | *required* | Shares filled | Progress |
| `average_price` | `float` | *required* | Average fill price | Execution quality |
| `slippage` | `float` | *required* | Slippage from target | Quality metric |
| `execution_time` | `datetime` | *required* | Completion time | Timing |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `OrderManagementService` | Order lifecycle |
| `ExecutionService` | Algorithmic execution |
| `BrokerConnectorService` | Exchange connectivity |

## Frontend Components
- Advanced order entry (FrontendOrders)
- Bracket order builder
- Execution monitor
