# Backend Service: REITs (The Property Stock Lab)

## Overview
The **REITs Service** provides specialized analytics for Real Estate Investment Trusts. It calculates the key metrics that differ from traditional equity analysis: FFO (Funds From Operations) and AFFO (Adjusted FFO).

## Core Components

### 1. FFO Calculator (`ffo_calculator.py`)
- **FFO**: Adds back non-cash depreciation to net income and subtracts gains on property sales.
- **AFFO**: Further adjusts FFO by subtracting recurring capital expenditures, providing a truer picture of sustainable cash flow.

### 2. Supporting Modules
- `payout_validator.py`: Checks if the REIT's dividend payout ratio is sustainable.
- `property_classifier.py`: Categorizes REITs by sector (Residential, Industrial, Retail, etc.).
- `sector_yield_tracker.py`: Compares yields across REIT sectors.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **REIT Analyzer** | FFO Comparison | `ffo_calculator.calculate_ffo()` | **Missing** (Data powers Research) |

## Usage Example

```python
from services.reits.ffo_calculator import FFOCalculator

calc = FFOCalculator()

# Calculate FFO for a REIT
ffo = calc.calculate_ffo(
    net_income=50_000_000,
    depreciation=20_000_000,
    gains_on_sales=5_000_000
)

# Calculate AFFO (truer cash flow)
affo = calc.calculate_affo(ffo, recurring_cap_ex=8_000_000)

print(f"FFO: ${ffo:,.2f}, AFFO: ${affo:,.2f}")
```
