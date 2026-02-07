# Backend Service: Operations (Efficiency Engine)

## Overview
The **Operations Service** is the "Cyborg" component of the Sovereign OS, designed to optimize the mix of human capital and automated systems. It provides quantitative frameworks for "Buy vs. Build" decisions (e.g., "Should we hire a Controller or use an outsourced firm?") and tracks the "Return on Effort" for various investment strategies to ensure scalability.

## Core Components

### 1. Outsource Calculator (`outsource_calc.py`)
The Hiring ROI logic.
- **Cost Comparison**: Maintains a database of industry standard salaries for Family Office roles (Controller, Accountant, Analyst) adjusting for benefits and overhead.
- **Volume-Based Tiers**: Compares internal fixed costs against variable outsourced vendor costs based on transaction volume.
- **Decision Engine**: Outputs a clear `HIRE_INTERNAL` vs `OUTSOURCE_FUNCTION` recommendation.

### 2. Workload Tracker (`workload_tracker.py`)
The Scalability Monitor.
- **Seat Management**: Tracks active licenses for expensive terminals (Bloomberg at $2,400/mo, Refinitiv at $1,800/mo) to identify unused assets.
- **Effort Scoring**: Aggregates "Research Hours" + "Monitoring Hours" + "Trading Minutes" per strategy.
    - *Scalability Heuristic*: If a strategy requires >20 hours/month of human intervention, it is flagged as `is_scalable: False`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Admin Console** | Resource Utilization | `workload_tracker.get_monthly_tech_burn()` | **Missing** |
| **Ops Dashboard** | Hiring vs Outsourcing ROI | `outsource_calc.evaluate_hiring_choice()` | **Missing** |

> [!NOTE]
> **Integration Status**: This service is currently a **Backend-Only** utility. Its logic is used for internal reporting and optimization but has not yet been exposed via a dedicated frontend dashboard.

## Dependencies
- `decimal`: For precise currency calculations in ROI modeling.
- `typing`: Standard type hinting.

## Usage Examples

### Evaluating a Hiring Decision
```python
from services.operations.outsource_calc import OperationsOutsourceCalculator

ops_calc = OperationsOutsourceCalculator()

# Evaluate hiring a Controller for a firm with 5,000 annual transactions
decision = ops_calc.evaluate_hiring_choice(
    function_name="CONTROLLER",
    transaction_vol=5000
)

print(f"Recommendation: {decision['recommendation']}")
print(f"Internal Cost: ${decision['estimated_internal_cost']:,.2f}")
print(f"Vendor Cost: ${decision['estimated_vendor_cost']:,.2f}")
```

### Checking Software Burn Rate
```python
from services.operations.workload_tracker import OperationalWorkloadService

tracker = OperationalWorkloadService()

# Assign seats
tracker.assign_seat(user_id="analyst_01", platform="BLOOMBERG")
tracker.assign_seat(user_id="pm_01", platform="REFINITIV")

# Calculate burn
monthly_burn = tracker.get_monthly_tech_burn()
print(f"Monthly Tech Fixed Costs: ${monthly_burn:,.2f}")
```
