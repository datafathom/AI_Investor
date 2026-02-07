# Backend Service: Philanthropy (The "Enough" Engine)

## Overview
The **Philanthropy Service** enforces the Sovereign Individual's "Enough" philosophy. It automatically sweeps capital above a defined Net Worth threshold (e.g., $3M) into charitable causes using tax-efficient structures. It integrates with crypto-native donation platforms (The Giving Block) and charity rating agencies (Charity Navigator) to ensure high-impact giving.

## Core Components

### 1. Donation Service (`donation_service.py`)
The Sweeper.
- **Excess Calculation**: `max(0, Current_Net_Worth - Threshold)`.
- **Routing Logic**: Splits excess capital according to user-defined allocations (e.g., "50% Climate, 30% Education, 20% Health").
- **Tax Optimization**: Tracks potential tax savings from donations to offset capital gains in other services.

### 2. Charity Client (`charity_client.py`)
The Connector.
- **The Giving Block**: Interface for executing crypto donations (ETH/BTC) directly to non-profits, avoiding capital gains tax on the appreciation.
- **Charity Navigator**: Fetches "Financial Health" and "Transparency" scores to gatekeep donations (no scams allowed).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Impact Dashboard** | Donation Router | `donation_service.route_excess_alpha()` | **Implemented** (`DonationRouter.jsx`) |
| **Philanthropy** | Charity Search | `charity_client.get_charity_rating()` | **Partially Implemented** (Mock data in `ImpactDashboard.jsx`) |

## Dependencies
- `httpx`: Async HTTP client for external API calls.
- `dataclasses`: Structuring donation records and allocation objects.

## Usage Examples

### Sweeping Excess Capital
```python
from services.philanthropy.donation_service import get_donation_service

service = get_donation_service()

# Assume net worth is $3.5M and threshold is $3.0M
excess = await service.calculate_excess_alpha(
    current_net_worth=3500000.0,
    threshold=3000000.0
)

if excess > 0:
    print(f"Excess Capital Detected: ${excess:,.2f}")
    
    # Route to causes
    record = await service.route_excess_alpha(
        amount=excess,
        allocations=[
            {"category": "Climate", "percentage": 50},
            {"category": "Education", "percentage": 50}
        ]
    )
    
    print(f"Donation Executed: {record.id}")
    print(f"Est. Tax Savings: ${record.tax_savings_est:,.2f}")
```

### Checking Charity Health
```python
from services.philanthropy.charity_client import CharityNavigatorClient

client = CharityNavigatorClient()

rating = await client.get_charity_rating("Doctors Without Borders")

print(f"Score: {rating['score']}/100")
print(f"Transparency: {rating['transparency']}")
```
