# Backend Service: Watchlist (The Radar)

## Overview
The **Watchlist Service** allows users to track symbols of interest across multiple organized lists. It supports alerts and integrates with market data for real-time updates.

## Core Components

### 1. Watchlist Service (`watchlist_service.py`)
- **CRUD Operations**: Create, read, update, delete watchlists.
- **Symbol Management**: Add and remove symbols from lists.
- **Multi-Watchlist Support**: Users can have multiple named watchlists.

### 2. Alert Service (`alert_service.py`)
- **Price Alerts**: Triggers when a symbol hits a target price.
- **Volume Alerts**: Triggers on unusual volume.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Sidebar** | Watchlist Panel | `watchlist_service` | **Implemented** |
| **Alerts Page** | Alert Manager | `alert_service` | **Partially Implemented** |

## Usage Example

```python
from services.watchlist.watchlist_service import get_watchlist_service
import asyncio

service = get_watchlist_service()

async def main():
    watchlist = await service.create_watchlist(
        user_id="user_123",
        watchlist_name="Tech Giants",
        symbols=["AAPL", "MSFT", "GOOGL"]
    )
    
    await service.add_symbol(watchlist.watchlist_id, "NVDA")
    print(f"Symbols: {watchlist.symbols}")

asyncio.run(main())
```
