# Backend Service: Real Estate (The Property Empire)

## Overview
The **Real Estate Service** manages direct property investments and syndicated real estate deals. It tracks K-1 distributions, calculates depreciation recapture for tax purposes, and monitors capital raise progress for GP/LP structures.

## Core Components

### 1. Syndication Service (`syndication_service.py`)
- **Capital Raise Tracker**: Monitors "soft circle" commitments from investors before a deal closes.
- **K-1 Distribution Tracker**: Records distributions and adjusts cost basis for "Return of Capital" events.
- **Depreciation Recapture Calculator**: At sale, calculates the portion of gain subject to depreciation recapture (taxed at 25%) vs. long-term capital gains.

### 2. Supporting Modules
- `rental_yield.py`: Cap rate and cash-on-cash return calculations.
- `timer_service.py`: Manages 1031 exchange deadlines.
- `liquidity_model.py`: Estimates time-to-exit for illiquid property holdings.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Real Estate Portfolio** | Syndication Manager | `syndication_service.get_raise_status()` | **Partially Implemented** |
| **Tax Planning** | Recapture Estimator | `syndication_service.calculate_tax_recapture()` | **Missing** |

## Usage Example

```python
from services.real_estate.syndication_service import SyndicationService
from decimal import Decimal

service = SyndicationService()

# Track a soft commitment
service.soft_circle("DEAL_123", "INVESTOR_A", Decimal("100000"))

# Check capital raise progress
status = service.get_raise_status("DEAL_123", Decimal("1000000"))
print(f"Raise Progress: {status['pct_complete']}%")
```
