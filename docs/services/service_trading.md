# Backend Service: Trading (The Execution Floor)

## Overview
The **Trading Service** contains **22 modules** for order execution, risk management, and trading simulation. It provides both live trading infrastructure and a realistic paper trading environment for strategy development.

## Core Components (Selected)

### 1. Paper Trading Service (`paper_trading_service.py`)
- **Virtual Portfolios**: Simulated portfolios with configurable starting capital.
- **Realistic Execution**: Slippage, commissions, and partial fills.
- **Performance Tracking**: Returns, drawdown, and position analytics.

### 2. FX Service (`fx_service.py`)
- Multi-currency trading and exposure management.

### 3. Option Hedge Service (`option_hedge_service.py`)
- Protective put and covered call strategies.

### Other Key Modules
- `trailing_stop.py`: Dynamic trailing stop-loss orders.
- `slippage_estimator.py`: Estimates execution slippage by order size.
- `defensive_protocol.py`: Risk-off protocols for market crashes.
- `ipo_tracker.py`: Tracks IPO allocations and lock-up periods.
- `beneficiary_blocker.py`: Prevents trades that violate beneficiary restrictions.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Paper Trading** | Portfolio View | `paper_trading_service.get_portfolio_performance()` | **Implemented** (`PaperTrading.jsx`) |
| **Order Ticket** | Execute Button | `paper_trading_service.execute_paper_order()` | **Implemented** |
| **FX Dashboard** | Currency Exposure | `fx_service` | **Implemented** (`FXOverview.jsx`) |

## Usage Example

```python
from services.trading.paper_trading_service import get_paper_trading_service
import asyncio

service = get_paper_trading_service()

async def main():
    # Create a paper trading portfolio
    portfolio = await service.create_virtual_portfolio(
        user_id="user_123",
        portfolio_name="My Test Strategy",
        initial_cash=100000.0
    )
    
    # Execute a paper trade
    order = await service.execute_paper_order(
        portfolio_id=portfolio.portfolio_id,
        symbol="AAPL",
        quantity=100,
        order_type="market"
    )
    
    print(f"Filled at ${order.filled_price:.2f}")
    print(f"Commission: ${order.commission:.2f}")
    print(f"Slippage: ${order.slippage:.4f}")

asyncio.run(main())
```
