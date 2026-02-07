# Backend Service: Wealth (The Net Worth Engine)

## Overview
The **Wealth Service** is a comprehensive wealth management hub with **26 modules** covering net worth tracking, asset allocation homeostasis, and specialized financial planning tools for UHNW families.

## Core Components (Selected)

### 1. Homeostasis Engine (`homeostasis_engine.py`)
- **Portfolio Balance**: Maintains target ratios between liquid growth (50%), safe moat (30%), and speculative (20%).
- **Deviation Detection**: Flags when allocations drift more than 5% from targets.
- **Rebalancing Actions**: Recommends specific adjustments.

### 2. Other Key Modules
- `net_worth.py`: Consolidated net worth calculation.
- `ppli_forecaster.py`: Private Placement Life Insurance projections.
- `bond_ladder.py`: Bond maturity ladder construction.
- `concentration_alert.py`: Single-position concentration warnings.
- `enough_calculator.py`: "Enough" wealth threshold calculation.
- `estate_planner.py`: Estate transfer optimization.
- `inflation_hedge.py`: Inflation protection strategies.
- `illiquid_tracker.py`: Tracks illiquid asset exposure.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Net Worth Dashboard** | Total Value | `net_worth` | **Implemented** |
| **Asset Allocation** | Homeostasis Gauge | `homeostasis_engine.check_homeostasis()` | **Partially Implemented** |
| **Estate Planning** | Transfer Optimizer | `estate_planner` | **Missing** |

## Usage Example

```python
from services.wealth.homeostasis_engine import HomeostasisEngine

engine = HomeostasisEngine()

portfolio = {
    "liquid_growth": 600000,
    "safe_moat": 300000,
    "speculative": 100000
}

result = engine.check_homeostasis(portfolio)
print(f"Balanced: {result['is_balanced']}")
print(f"Actions: {result['actions_required']}")
```
