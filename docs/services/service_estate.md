# Backend Service: Estate

## Overview
The **Estate Service** is the platform's legacy preservation and multi-generational transfer engine. It enables clients to architect complex estate plans, simulate inheritance outcomes across decades, and enforce idiosyncratic trust stipulations (e.g., spendthrift clauses, milestone-based payouts). It includes specialized calculators for estate taxes, probate fees, and generation-skipping transfer (GST) impacts.

## Core Components

### 1. Estate Planning Engine (`estate_planning_service.py`)
The central orchestrator for legacy architecture.
- **Beneficiary Management**: Manages primary and contingent beneficiaries with precise allocation percentages.
- **Tax Optimization**: Automatically calculates estimated Federal Estate Tax based on current exemptions ($12M+ in 2024) and progressive tax brackets (up to 40%).
- **Asset Allocation**: Maps the total portfolio value to specific beneficiary buckets in real-time.

### 2. Inheritance Simulator (`inheritance_simulator.py`)
A predictive tool for long-term legacy visualization.
- **Wealth Projection**: Simulates the compound growth of an estate (defaulting to 6% CAGR) over 10-30 years.
- **After-Tax Projections**: Calculates the actual "net-to-heir" inheritance after accounting for spousal exemptions and potential inheritance taxes.
- **Scenario Modeling**: Allows users to compare different estate architectures (e.g., "Full Trust" vs. "Direct Transfer") side-by-side.

### 3. Trust Stipulations & Clauses (`stipulation_service.py`)
Enforces the specific "rules of the legacy."
- **Clause Management**: Stores and retrieves behavioral stipulations for trusts, such as "Crummey" notices or "Spendthrift" provisions.
- **Milestone Triggers**: Supports condition-based distributions (e.g., distributions triggered by reaching a certain age or graduating from an accredited university).

### 4. Beneficiary Waterfall (`beneficiary_tree.py`)
- **Primary & Contingent Logic**: Validates that beneficiary waterfalls sum to 100% and correctly handle contingent paths if primary beneficiaries are unavailable.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Estate Dashboard** | Beneficiary Waterfall Tree | `beneficiary_tree.validate()` |
| **Estate Dashboard** | Tax Liability Pulse | `estate_planning_service.calculate_estate_tax()` |
| **Inheritance View** | Multi-Decade Projection Chart | `inheritance_simulator.simulate_inheritance()` |
| **Trust Setup Wizard** | Clause Library | `stipulation_service.get_stipulations()` |
| **Planning Station** | Scenario Comparison Grid | `inheritance_simulator.compare_scenarios()` |

## Dependencies
- `schemas.estate`: Defines the complex Pydantic models for `EstatePlan`, `Beneficiary`, and `InheritanceProjection`.
- `services.portfolio.portfolio_aggregator`: Streams real-time portfolio value as the baseline for estate calculations.
- `services.system.cache_service`: Provides low-latency storage for active estate plans and simulation results.

## Usage Examples

### Running a 20-Year Inheritance Simulation
```python
from services.estate.inheritance_simulator import get_inheritance_simulator

sim = get_inheritance_simulator()

# Project current estate plan 20 years into the future
projections = await sim.simulate_inheritance(
    plan_id="estate_plan_jones_001",
    projection_years=20
)

for p in projections:
    print(f"Beneficiary: {p.beneficiary_id}")
    print(f"Estimated Pre-Tax: ${p.projected_inheritance:,.2f}")
    print(f"Estimated After-Tax: ${p.after_tax_inheritance:,.2f}")
```

### Adding a Milestone-Based Stipulation
```python
from services.estate.stipulation_service import StipulationService
from uuid import uuid4

stip_svc = StipulationService()
trust_id = uuid4()

# Add a university graduation requirement
stip_svc.add_stipulation(
    trust_id=trust_id,
    clause_type="MILESTONE",
    description="Recipient must graduate from an accredited university before first payout.",
    trigger_condition="degree_verification == True"
)
```
