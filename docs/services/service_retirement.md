# Backend Service: Retirement (The Glide Path)

## Overview
The **Retirement Service** provides the core financial planning engine for retirement projections. It uses **Monte Carlo simulations** (10,000 runs) to calculate the probability of a successful retirement based on savings rate, expected returns, and withdrawal strategy.

## Core Components

### 1. Retirement Projection Service (`retirement_projection_service.py`)
- **Monte Carlo Engine**: Runs thousands of simulations to model uncertainty.
- **Scenario Comparison**: Allows comparison of multiple retirement scenarios (e.g., retiring at 60 vs. 65).
- **Year-by-Year Timeline**: Generates a deterministic projection for visualization.

### 2. Supporting Modules (18 total)
- `glide_path_engine.py`: Automatically de-risks asset allocation as retirement approaches.
- `safe_withdrawal.py`: Implements the classic 4% rule and variants.
- `sequence_risk.py`: Models the risk of bad returns early in retirement.
- `match_calculator.py`: Calculates optimal 401(k) contributions to maximize employer match.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Retirement Dashboard** | Monte Carlo Chart | `retirement_projection_service.project_retirement()` | **Implemented** (`RetirementGauge.jsx`) |
| **Planning Widget** | Scenario Comparator | `retirement_projection_service.compare_scenarios()` | **Implemented** |

## Usage Example

```python
from services.retirement.retirement_projection_service import get_retirement_projection_service
from schemas.retirement import RetirementScenario

service = get_retirement_projection_service()

scenario = RetirementScenario(
    scenario_name="Early Retirement",
    current_age=40,
    retirement_age=55,
    life_expectancy=90,
    current_savings=500000.0,
    annual_contribution=30000.0,
    expected_return=0.07,
    withdrawal_rate=0.035,
    inflation_rate=0.03
)

projection = await service.project_retirement(scenario)
print(f"Probability of Success: {projection.probability_of_success:.1%}")
print(f"Projected Savings at Retirement: ${projection.projected_retirement_savings:,.0f}")
```
