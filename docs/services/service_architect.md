# Backend Service: Architect

## Overview
The **Architect Service** is responsible for long-term strategic wealth modeling. It provides the "Financial Fortress" logic used to project net worth over several decades, adjusting for inflation, taxes, and lifestyle changes to determine critical milestones such as the **Year of Financial Independence (FI Year)**.

## Core Components

### Life-Cycle Service (`life_cycle_service.py`)
This component simulates the long-term architectural health of a user's financial life.

#### Classes

##### `LifeCycleService`
A high-performance simulator designed to project financial trajectories over a 50-year horizon.

**Methods:**
- `run_simulation(current_nw, monthly_savings, monthly_burn, expected_return, inflation, horizon_years, current_age) -> ProjectionResult`
    - **Purpose**: Runs a deterministic simulation of wealth accumulation and depletion.
    - **Logic**:
        - **4% Rule Integration**: Automatically calculates the FI Year when 4% of net worth exceeds annual spending.
        - **Inflation Adjustments**: Dynamically scales the "burn rate" (spending) each year to account for purchasing power decay.
        - **Performance**: Guaranteed execution time of under 1 second for instant UI responsiveness.
    - **Returns**: A `ProjectionResult` containing year-by-year paths for net worth, real spending, and critical age/year milestones.

## Dependencies
- `math`: Used for compound growth and exponential spending calculations.
- `dataclasses`: Defines the structured `ProjectionResult` output.

## Usage Example

### Calculating Financial Independence
```python
from services.architect.life_cycle_service import get_lifecycle_service

architect = get_lifecycle_service()
result = architect.run_simulation(
    current_nw=500000.0,
    monthly_savings=5000.0,
    monthly_burn=4000.0,
    expected_return=0.08,
    inflation=0.03,
    current_age=35
)

if result.fi_year:
    print(f"Projected FI Year: {result.fi_year} (Age: {result.fi_age})")
    print(f"Final Net Worth (Year 50): ${result.net_worth[-1]:,.2f}")
else:
    print("FI not achieved within the 50-year horizon.")
```
