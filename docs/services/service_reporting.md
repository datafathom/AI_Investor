# Backend Service: Reporting (The Family Office Statement)

## Overview
The **Reporting Service** generates consolidated reports for high-net-worth individuals and family offices. It aggregates assets across complex structures (trusts, insurance wrappers, private placements) into a single "Total Wealth" view.

## Core Components

### 1. Total Wealth Calculator (`total_wealth.py`)
- **Unified Balance Sheet**: Combines liquid assets, trust assets, insurance cash value (PPLI), and private placements.
- **Liquidity Scoring**: Calculates the percentage of assets that can be converted to cash quickly.
- **Qualification Status**: Flags clients as "Qualified Purchaser" (> $5M) for regulatory access to certain investments.

### 2. Supporting Modules
- `global_risk_aggregator.py`: Summarizes risk exposure across all entities.
- `trust_vs_probate.py`: Compares estate costs with and without trust structures.
- `survival_score.py`: Calculates a client's "runway" (months of expenses covered by liquid assets).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Wealth Dashboard** | Net Worth Summary | `total_wealth.aggregate_net_worth()` | **Implemented** (Global Store) |
| **Reports Page** | PDF Export | Various reporting modules | **Partially Implemented** |

## Usage Example

```python
from services.reporting.total_wealth import TotalWealthCalculator
from decimal import Decimal

calc = TotalWealthCalculator()

report = calc.aggregate_net_worth(
    liquid_assets=Decimal("5000000"),
    trust_assets=Decimal("10000000"),
    insurance_cash_value=Decimal("2000000"),
    private_placements=Decimal("3000000")
)

print(f"Total Net Worth: ${report['total_net_worth']:,.2f}")
print(f"Alternative Exposure: {report['alternative_exposure_pct']}%")
print(f"Status: {report['status']}")
```
