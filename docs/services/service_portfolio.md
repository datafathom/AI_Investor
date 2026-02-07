# Backend Service: Portfolio (The Ledger)

## Overview
The **Portfolio Service** is the central source of truth for the Sovereign Individual's Net Worth. It solves the "fragmentation problem" by aggregating real-time positions from multiple brokerage APIs (Alpaca, Robinhood, IBKR) and combining them with manually tracked illiquid assets (Real Estate, Art, PE). It provides the unified data layer that powers all higher-level analytics (Risk, Performance, Planning).

## Core Components

### 1. Portfolio Aggregator (`portfolio_aggregator.py`)
The Unifier.
- **Multi-Broker Connectivity**: Polling engine that fetches positions from connected exchange APIs.
- **Unified Schema**: Normalizes different API responses (e.g., Alpaca's `qty` vs IBKR's `position`) into a standard `Position` object with standardized cost basis and P&L calculations.
- **Caching**: Reduces API rate limits by caching the aggregated view for a short duration (e.g., 60s).

### 2. Assets Service (`assets_service.py`)
The Illiquid Manager.
- **Manual CRUD**: Simple database (JSON-backed) for tracking assets that don't have APIs (Homes, Cars, Angel Investments).
- **Valuation Updates**: Allows users to manually update the estimated value of these assets to keep Net Worth accurate.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Institutional Dashboard** | Allocation Wheel | `portfolio_aggregator.calculate_unified_gains()` | **Implemented** (`AssetAllocationWheel.jsx`) |
| **All Pages** | Total Net Worth | `portfolio_aggregator.get_portfolio()` | **Implemented** (Global Store) |
| **Illiquid Assets** | Asset Editor | `assets_service.add_asset()` | **Partially Implemented** (`Assetlist` pending) |

## Dependencies
- `collections.defaultdict`: Used for efficient aggregation of positions across multiple accounts (e.g., summing AAPL shares from Robinhood and Alpaca).
- `services.brokerage`: heavily relies on the Brokerage Service clients.

## Usage Examples

### Fetching the Unified Portfolio
```python
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator

aggregator = get_portfolio_aggregator()

# Get combined view of Crypto, Equities, and Cash
portfolio = await aggregator.aggregate_positions(
    user_id="user_01",
    include_alpaca=True,
    include_robinhood=True,
    include_ibkr=False
)

print(f"Total Net Worth: ${portfolio['total_current_value']:,.2f}")
print(f"Unrealized Gain: ${portfolio['total_unrealized_gain']:,.2f}")

for pos in portfolio['positions']:
    print(f"- {pos['symbol']}: {pos['quantity']} shares via {pos['sources']}")
```

### Adding a Physical Asset
```python
from services.portfolio.assets_service import assets_service

# Add a rental property
assets_service.add_asset({
    "name": "Downtown Condo",
    "category": "Real Estate",
    "value": 450000.00,
    "location": "Austin, TX",
    "purchaseDate": "2023-06-15"
})

print(f"Updated Illiquid Value: ${assets_service.get_total_valuation():,.2f}")
```
