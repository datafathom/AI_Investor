# Backend Service: Strategy (The Execution Engine)

## Overview
The **Strategy Service** is the runtime environment for trading strategies. It takes the "recipes" defined in the Strategies service and actually executes them live, with risk controls, performance monitoring, and drift detection.

## Core Components

### 1. Strategy Execution Service (`strategy_execution_service.py`)
- **Lifecycle Management**: Start, stop, and pause strategies.
- **Rule Execution**: Evaluates conditions and executes actions based on priority.
- **Performance Tracking**: Calculates win rate, P&L, Sharpe, and drawdown.
- **Drift Detection**: Calculates statistical drift between backtested expectations and live performance using chi-square and KS tests.

### 2. Supporting Modules
- `strategy_builder_service.py`: Creates and configures strategies.
- `strategy_compiler.py`: Compiles strategy rules into executable form.
- `tax_harvester.py`: Automated tax-loss harvesting logic.
- `dynamic_allocator.py`: Adjusts allocations based on market conditions.
- `rebalance_engine.py`: Triggers rebalancing when drift exceeds thresholds.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategy Dashboard** | Run/Stop Controls | `strategy_execution_service.start_strategy()` | **Implemented** |
| **Performance Tab** | Drift Monitor | `strategy_execution_service.calculate_model_drift()` | **Partially Implemented** |

## Usage Example

```python
from services.strategy.strategy_execution_service import get_strategy_execution_service
import asyncio

service = get_strategy_execution_service()

async def main():
    # Start a strategy
    strategy = await service.start_strategy(
        strategy_id="strat_001",
        portfolio_id="portfolio_main"
    )
    print(f"Strategy {strategy.strategy_id} is now {strategy.status.value}")
    
    # Check for drift
    drift = await service.calculate_model_drift("strat_001")
    print(f"Drift Score: {drift.drift_score:.2%} - Status: {drift.status}")

asyncio.run(main())
```
