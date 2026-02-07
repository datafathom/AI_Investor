# Backend Service: Execution

## Overview
The **Execution Service** is the platform's high-fidelity trading and settlement hub. It is responsible for transforming high-level investment decisions into optimal market orders while minimizing slippage, hiding institutional intent (IcebergING), and adhering to specific execution benchmarks like **VWAP** (Volume-Weighted Average Price) and **TWAP** (Time-Weighted Average Price).

## Core Components

### 1. Smart Execution Engine (`smart_execution_service.py`)
The platform's dedicated algorithm suite for trade optimization.
- **VWAP / TWAP Execution**: Automatically slices large parent orders into child orders based on historical volume profiles (U-Shape) or fixed time intervals to achieve benchmark targets.
- **Implementation Shortfall**: Provides a "Patient-to-Urgent" slider logic that balances the risk of market impact (slippage) against the risk of delayed execution.

### 2. Smart Order Router (SOR) (`smart_sor.py`)
Determines the *how* and *where* of order routing.
- **Iceberg Orders**: Automatically fragments orders exceeding specified thresholds (e.g., 500 shares) to hide the true size of institutional trades from public order books.
- **Volatility-Aware Routing**: Switches between **Limit Orders** (to protect price in high-volatility regimes) and **Market Orders** (for immediate liquidity in stable regimes).

### 3. Algo Engine (`algo_execution.py`)
The mathematical generator for execution schedules.
- **Volume Profiling**: Utilizes a tiered "bucket" approach to model intraday liquidity, ensuring that order intensity matches expected market volume (e.g., morning and close intensity).

### 4. Philanthropy Execution (`philanthropy_service.py`)
- **Impact Trades**: Manages the specialized execution of trades intended for charitable impact, potentially involving tax-efficient "In-Kind" asset donations and specialized settlement workflows.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Order Ticket (Advanced) | `smart_sor.determine_order_strategy()` |
| **Trading Terminal** | Execution Progress Pulse | `smart_execution_service.execute_twap()` |
| **Order History** | Slippage Auditor | `execution_result.market_impact` |
| **Impact Hub** | Charitable Trade Wizard | `philanthropy_service` (Trade settlement) |
| **Admin Panel** | Algo Baseline Config | `algo_engine.DEFAULT_VOLUME_PROFILE` |

## Dependencies
- `schemas.orders`: Defines the standard `ExecutionStrategy` and `ExecutionResult` types.
- `services.system.cache_service`: Maintains real-time state for active execution schedules.
- `MarketDataService`: (Integration) Supplies real-time volatility and volume metrics for SOR decisions.

## Usage Examples

### Dispatching a VWAP Execution Schedule
```python
from services.execution.smart_execution_service import get_smart_execution_service

exec_svc = get_smart_execution_service()

# Execute 10,000 shares of SPY over 2 hours using VWAP
executions = await exec_svc.execute_vwap(
    symbol="SPY",
    total_quantity=10000,
    time_window_minutes=120
)

for ex in executions:
    print(f"Slice Filled: {ex.filled_quantity} @ ${ex.average_price:.2f} | Strategy: {ex.execution_strategy}")
```

### Determining Optimal Order Strategy via SOR
```python
from services.execution.smart_sor import get_sor

sor = get_sor()

# 5,000 shares in a high-volatility market (4%)
strategy = sor.determine_order_strategy(
    symbol="TSLA",
    quantity=5000,
    volatility=0.04
)

print(f"Routing Style: {strategy['execution_style']}") # Likely ICEBERG
print(f"Order Type: {strategy['order_type']}")         # Likely LIMIT
print(f"Reason: {strategy.get('reason', 'N/A')}")
```
