# Backend Service: Social Trading (The Mirror)

## Overview
The **Social Trading Service** enables users to automatically replicate the trades of other investors. It provides the infrastructure for "copy trading," where a follower's portfolio mirrors the positions of a leading trader, adjusted by risk parameters.

## Core Components

### 1. Copy Trading Service (`copy_trading_service.py`)
- **Config Management**: Creates and manages copy relationships between followers and traders.
- **Proportional Allocation**: Scales trade size based on follower's chosen percentage of capital.
- **Risk Multiplier**: Allows followers to amplify or reduce the copied position size.
- **Execution Engine**: Automatically mirrors trades for all active followers.

### 2. Social Trading Service (`social_trading_service.py`)
- Manages trader profiles and leaderboards.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Social Trading Dashboard** | Copy Button | `copy_trading_service.create_copy_config()` | **Implemented** |
| **Leaderboards** | Top Traders | `social_trading_service` | **Implemented** |

## Usage Example

```python
from services.social_trading.copy_trading_service import get_copy_trading_service
import asyncio

service = get_copy_trading_service()

async def main():
    # Start copying a trader
    config = await service.create_copy_config(
        follower_id="user_123",
        trader_id="trader_alpha",
        allocation_percentage=25.0,  # Use 25% of my capital
        risk_multiplier=0.5          # Take half-sized positions
    )
    print(f"Copying {config.trader_id} with config {config.config_id}")

asyncio.run(main())
```
