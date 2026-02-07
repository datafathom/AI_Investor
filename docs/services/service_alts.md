# Backend Service: Alts (Physical Assets)

## Overview
The **Alts Service** (Alternative Assets) focuses on the "Negative Carry" and maintenance costs associated with physical alternative investments such as Art, Luxury Watches, Fine Wine, and self-custodied Crypto hardware.

## Core Components

### Alts Cost Tracker (`cost_tracker.py`)
This component tracks the ongoing expenses required to maintain and insure high-value physical assets.

#### Classes

##### `AltsCostTracker`
Calculates insurance premiums and storage fees based on asset type and current market value.

**Methods:**
- `calculate_annual_maintenance(asset_id: str, value: float, asset_type: str) -> Dict[str, Any]`
    - **Purpose**: Determines the total annual "Carry Cost" for a physical asset.
    - **Insurance logic**:
        - **ART**: 1% of value.
        - **WATCH**: 0.8% of value.
        - **WINE**: 0.5% of value.
        - **CRYPTO_HW**: 2% of value (due to elevated security risks).
    - **Storage logic**: Simulations incorporate flat monthly fees (e.g., $100/mo) for specialized vaulting.
    - **Returns**: A detailed breakdown of insurance, storage, and total carry as a percentage of asset value.

## Dependencies
- `decimal`: Ensures precision in cost aggregation.
- `logging`: Tracks maintenance audits and carry-cost updates.

## Usage Example

### Calculating Carry Cost for a Watch
```python
from services.alts.cost_tracker import AltsCostTracker

tracker = AltsCostTracker()
report = tracker.calculate_annual_maintenance(
    asset_id="PATEK-5711", 
    value=150000.0, 
    asset_type="WATCH"
)

print(f"Total Negative Carry: ${report['total_carry_cost']:,.2f}")
print(f"Annual Carry %: {report['carry_pct']}%")
```
