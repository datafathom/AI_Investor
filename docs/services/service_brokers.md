# Backend Service: Brokers (Specific)

## Overview
The **Brokers Service** directory houses specialized modules for brokerage simulation and multi-account data aggregation. These components are essential for the system's "Paper Trading" mode and for generating a holistic view of wealth across fragmented brokerage accounts.

## Core Components

### 1. Demo Broker Service (`demo_broker.py`)
A high-fidelity simulator that provides a risk-free environment for testing algorithms.
- **Role**: Emulates a live brokerage for paper trading.
- **Internal State Management**:
    - **Balance & Equity**: Maintains a virtual cash balance and tracks total equity.
    - **Position Tracking**: Manages a dictionary of open positions, calculating **weighted average buy prices** on every trade to ensure realistic P&L reporting.
- **Execution Logic**: Supports a "Market Order" execution model that immediately fills orders at specified mock prices, updating the internal ledger synchronously.
- **Lifecycle Support**: Includes a `reset_account` feature to clear all positions and return the virtual balance to a baseline (e.g., $100,000) for new testing cycles.

### 2. Broker Aggregator (`aggregator.py`)
Provides a consolidated view of the user's total brokerage footprint.
- **Purpose**: Combines disparate data streams from multiple registered broker instances.
- **Capabilities**:
    - **Equity Consolidation**: Calculates `total_equity` by summing the equity reported across all linked brokers (e.g., aggregating values from Alpaca, IBKR, and Robinhood).
    - **Position Mapping**: Flattens all account positions into a single unified list, enabling system-wide asset concentration analysis.

## Usage Examples

### Executing a Simulated Trade in Demo Mode
```python
from services.brokers.demo_broker import DemoBrokerService

demo = DemoBrokerService()

# Simulate a market buy of 10 shares of TSLA at $200
trade = demo.execute_market_order(
    symbol="TSLA",
    side="BUY",
    quantity=10,
    current_price=200.00
)

summary = demo.get_account_summary()
print(f"New Balance: ${summary['balance']}")
print(f"Position: {summary['positions']['TSLA']}")
```

### Aggregating Multi-Account Equity
```python
from services.brokers.aggregator import BrokerAggregator

agg = BrokerAggregator()

# Register data from different accounts
agg.register_broker("alpaca_personal", {"equity": 50000.00, "positions": [{"symbol": "AAPL", "qty": 100}]})
agg.register_broker("ibkr_joint", {"equity": 150000.00, "positions": [{"symbol": "SPY", "qty": 500}]})

total_wealth = agg.get_total_equity()
print(f"Total Brokerage Equity: ${total_wealth:,.2f}")
```
