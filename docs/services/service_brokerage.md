# Backend Service: Brokerage

## Overview
The **Brokerage Service** is the platform's multi-institutional orchestration layer. It abstracts the complexities of various brokerage APIs (Alpaca, IBKR, Robinhood) into a unified interface, enabling global asset execution, real-time position synchronization, and professional-grade risk management.

## Core Abstractions

### 1. The Universal Connector (`brokerage_service.py`)
This is the master registry of all connected financial institutions.
- **Support Matrix**:
    - **Execution**: Alpaca, Interactive Brokers, TradeStation.
    - **Aggregation**: Fidelity, Charles Schwab, Vanguard, E*TRADE.
    - **Crypto**: Coinbase, Kraken, Binance.US.
- **Role**: Manages the lifecycle of multiple concurrent brokerage connections and provides consolidated account status (e.g., total buying power across all linked vendors).

### 2. Specialized Execution Clients
The service provides dedicated clients for specific institutional needs:
- **Alpaca Client (`alpaca_client.py`)**: Optimized for automated US equity trading, supporting fractional shares and high-frequency order submission to both Paper and Live markets.
- **IBKR Client (`ibkr_client.py`)**: A professional-grade client for Interactive Brokers.
    - **Global Reach**: Access to 150+ markets across equities, options, futures, and forex.
    - **Deep Analytics**: Provides detailed **Margin Requirements**, **Currency Exposure**, and multi-asset position summaries.

### 3. Execution Engine & Safety Framework (`execution_service.py`)
The "Last Mile" of the trade lifecycle where orders are validated before being sent to the market.
- **Pre-Flight Safety Checks**:
    - **System Kill Switch**: Blocks all order routing if a global `SYSTEM_HALTED` flag is detected.
    - **Risk Limit Validation**: Rejects orders that violate defined parameters (e.g., maximum order quantity or exposure limits).
- **Routing Logic**: Dynamically maps trade intents to the most appropriate brokerage client based on asset class and account configuration.

### 4. Post-Trade Lifecycle
- **Position Sync (`position_sync.py`)**: Ensures the internal "Sovereign Book" matches the real-time holdings reported by the brokers.
- **Settlement Service (`settlement_service.py`)**: Tracks the transition of trades from execution to final cash settlement (T+1/T+2).

## Dependencies
- `alpaca-trade-api`: Powers the primary automated execution logic.
- `ib_insync` / `ibapi`: Interfaces with the Interactive Brokers Gateway/TWS.
- `services.system.secret_manager`: Securely retrieves and rotates institutional API keys.

## Usage Examples

### Fetching Consolidated Buying Power
```python
from services.brokerage.brokerage_service import get_brokerage_service

brokerage = get_brokerage_service()
status = brokerage.get_status()

print(f"Summary: {status['summary']}")
for conn in status['connections']:
    print(f"- {conn['name']}: {conn['status']}")
```

### Routing a Safety-Checked Order
```python
from services.brokerage.execution_service import get_execution_service

execution = get_execution_service()

# Order payload
order_intent = {
    "symbol": "NVDA",
    "qty": 50,
    "side": "buy",
    "type": "market"
}

# The engine performs risk checks and kill-switch checks before routing
result = execution.place_order(order_intent)

if result['status'] == "FILLED":
    print(f"Trade successful. ID: {result['order_id']}")
elif result['status'] == "REJECTED":
    print(f"Safety Violation: {result['reason']}")
```
