# Backend Service: Tax (The Tax Shelter)

## Overview
The **Tax Service** is the largest service in the platform with **49 specialized modules** dedicated to tax optimization, compliance, and planning. It handles everything from tax-loss harvesting to estate tax calculations, ensuring maximum after-tax returns for UHNW clients.

## Core Components (Selected)

### 1. Tax Optimization Service (`tax_optimization_service.py`)
- **Lot Selection**: FIFO, LIFO, Highest Cost, Lowest Cost, Specific Lot.
- **Year-End Projection**: Projects tax liability based on realized gains.
- **Withdrawal Sequencing**: Optimizes withdrawal order (taxable → tax-deferred → tax-free).

### 2. Harvest Services (`harvest_service.py`, `enhanced_tax_harvesting_service.py`)
- **Tax-Loss Harvesting**: Identifies losing positions to realize losses.
- **Wash Sale Protection**: Prevents wash sale violations.

### 3. Other Key Modules
- `qoz_service.py`: Qualified Opportunity Zone capital gains deferral.
- `section121_validator.py`: Primary residence sale exclusion ($250k/$500k).
- `exit_tax_engine.py`: Expatriation tax calculations.
- `backdoor_roth_procedure.py`: Mega Backdoor Roth IRA conversions.
- `crt_deduction.py`: Charitable Remainder Trust deductions.
- `gst_calculator.py`: Generation-Skipping Transfer Tax.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Tax Dashboard** | Harvest Opportunities | `harvest_service` | **Implemented** (`TaxOptimizer.jsx`) |
| **Tax Projection** | Year-End Estimate | `tax_optimization_service.project_year_end_tax()` | **Implemented** |
| **Withdrawal Planner** | Sequence Optimizer | `tax_optimization_service.optimize_withdrawal_sequence()` | **Partially Implemented** |

## Usage Example

```python
from services.tax.tax_optimization_service import get_tax_optimization_service
import asyncio

service = get_tax_optimization_service()

async def main():
    # Optimize lot selection for selling AAPL
    result = await service.optimize_lot_selection(
        portfolio_id="portfolio_001",
        symbol="AAPL",
        quantity=100,
        method="highest_cost"  # Minimize taxes on gains
    )
    
    print(f"Tax Impact: ${result['tax_impact']['tax_impact']:.2f}")
    print(f"Gain/Loss: ${result['gain_loss']:.2f}")

asyncio.run(main())
```
