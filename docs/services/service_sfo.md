# Backend Service: SFO (Single Family Office Hub)

## Overview
The **SFO Service** provides the economic justification and governance framework for Ultra High Net Worth (UHNW) families considering the transition from external advisors to a dedicated Single Family Office.

## Core Components

### 1. SFO Justification Engine (`sfo_justification.py`)
- **Breakeven Analysis**: Compares external RIA fees (~1% AUM) against internal staffing costs (~$1M base).
- **Complexity Premium**: Adds cost for every $100M over $1B AUM.
- **Viability Score**: Returns whether an SFO is economically justified.

### 2. Supporting Modules
- `governance.py`: Governance policies and voting structures.
- `dark_asset_service.py`: Tracks off-the-books or undisclosed assets.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Family Office Dashboard** | Breakeven Calculator | `sfo_justification.run_breakeven_analysis()` | **Missing** |

## Usage Example

```python
from services.sfo.sfo_justification import SFOJustificationEngine
from decimal import Decimal

engine = SFOJustificationEngine()

result = engine.run_breakeven_analysis(Decimal("500000000")) # $500M AUM

print(f"External Fees: ${result['external_annual_fees']:,.2f}")
print(f"Internal Costs: ${result['internal_operating_est']:,.2f}")
print(f"Is SFO Viable? {result['is_sfo_economically_viable']}")
```
