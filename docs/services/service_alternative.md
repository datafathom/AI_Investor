# Backend Service: Alternative

## Overview
The **Alternative Assets Service** specializes in mapping liquidity and valuation dynamics within the Private Equity (PE) secondary markets. It provides tools for investors to evaluate "Discount to NAV" opportunities and track critical fund exit windows.

## Core Components

### PE Secondary Service (`pe_secondary_service.py`)
This component models the secondary market for private equity interests, focusing on arbitrage opportunities and redemption logistics.

#### Classes

##### `PESecondaryService`
Handles the quantitative analysis of secondary market listings and LP (Limited Partner) obligations.

**Methods:**
- `calculate_nav_discount(reported_nav: Decimal, secondary_ask: Decimal) -> Dict[str, Any]`
    - **Purpose**: Calculates the percentage discount of a secondary market ask price relative to the fund's reported Net Asset Value (NAV).
    - **Logic**: Flags any discount greater than 30% as a "HIGH" opportunity rank.
    - **Returns**: A breakdown of the NAV, Ask, and calculated discount percentage.
- `track_redemption_window(fund_id: str, lockup_expiry: str) -> Dict[str, Any]`
    - **Purpose**: Tracks the time remaining until a fund's lockup period expires.
    - **Usage**: Essential for liquidity planning and identifying when LPs may be susceptible to "forced-seller" dynamics.

## Dependencies
- `decimal`: Used for high-precision financial calculations.
- `logging`: Records secondary market transactions and timer events.

## Usage Example

### Evaluating a Secondary Listing
```python
from decimal import Decimal
from services.alternative.pe_secondary_service import PESecondaryService

pe_svc = PESecondaryService()
result = pe_svc.calculate_nav_discount(
    reported_nav=Decimal("1000000.00"), 
    secondary_ask=Decimal("650000.00")
)

print(f"Opportunity: {result['opportunity_rank']} ({result['discount_pct']}% Discount)")
```
