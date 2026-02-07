# Backend Service: Broker

## Overview
The **Broker Service** acts as the "Hands" of the Sovereign OS, providing the execution layer for traditional brokerage platforms. It translates high-level investment decisions into low-level API calls for order placement, position monitoring, and multi-asset account management.

## Core Components

### Robinhood Service (`robinhood_service.py`)
A specialized interface for the Robinhood platform, supporting equities, options, and cryptocurrency.

#### Classes

##### `RobinhoodService`
A wrapper around the `robin_stocks` library that manages session lifecycle and transactional logic.

**Core Capabilities:**
- **Dynamic Authentication**: Supports username/password login combined with **TOTP-based 2-Factor Authentication (2FA)** for secure session initialization.
- **Account Intelligence**: Fetches real-time "Buying Power," cash balances, and total portfolio equity.
- **Position Enrichment**: Retrieves all open stock and crypto positions, automatically enriching them with ticker symbols and current cost-basis data.
- **Transactional Execution**: Provides simplified methods for placing market buy and sell orders with integrated error logging and status tracking.
- **Safety Mechanism**: Includes a full **Mock Mode** enabling safe end-to-end testing of trading workflows without risking real capital.

## Dependencies
- `robin_stocks`: The underlying library for Robinhood API communication.
- `utils.core.config`: Manages the secure retrieval of brokerage credentials from environment variables.

## Usage Examples

### Fetching Portfolio Buying Power
```python
from services.broker.robinhood_service import RobinhoodService

broker = RobinhoodService()
if broker.login():
    profile = broker.get_account_profile()
    print(f"Current Buying Power: ${profile['buying_power']}")
```

### Executing a "Safety-First" Market Order
```python
from services.broker.robinhood_service import RobinhoodService

# Initialize in Mock Mode for testing
broker = RobinhoodService(mock=True)

order = broker.place_market_order(
    symbol="AAPL", 
    quantity=1.0, 
    side="buy"
)

if "error" not in order:
    print(f"Mock Order Success: {order['id']} at ${order['price']}")
```
