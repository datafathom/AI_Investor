# Backend Service: HR

## Overview
The **HR Service** is a specialized personnel management engine tailored for the unique requirements of **Family Offices**. Unlike traditional corporate HR systems, this service focuses on "Heir Governance," institutional role management for descendants, and the balancing of hard performance KPIs with familial discretion. It is designed to track "Social Maintenance" value and identify structural nepotism within the family's enterprise holdings.

## Core Components

### 1. Heir Governance Engine (`heir_governance_svc.py`)
Manages the employment and compensation lifecycle for family descendants.
- **Productivity Evaluation**: Audits heir roles by comparing their discretionary salary against market-rate averages. It enforces a transparency policy that flags any role with a >1.5x pay premium as a "Cushey Job" (Nepotism), allowing for clear distinction between market-aligned roles and family support roles.
- **Discretionary KPI Overrides**: Implements a nuanced performance scoring system that balances "Hard KPIs" (40% weight) with "Family Discretion" (60% weight). This allows family principals to maintain executive control over internal performance metrics for family members.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Governance Hub** | Heir Productivity Audit | `heir_governance_svc.evaluate_role_productivity()` |
| **Governance Hub** | KPI Discretion Slider | `heir_governance_svc.apply_discretionary_kpi_override()` |
| **Family Ops Detail** | Staff Premium Ledger | `heir_governance_svc.evaluate_role_productivity()` |
| **Admin Station** | Nepotism Risk Heatmap | `heir_governance_svc` (Status flags) |

## Dependencies
- `logging`: Records audit logs of role flags (Nepotism) and discretionary overrides for historical governance transparency.

## Usage Examples

### Auditing an Heir's Role Premium
```python
from services.hr.heir_governance_svc import HeirGovernanceService
from uuid import uuid4

hr_svc = HeirGovernanceService()
heir_id = uuid4()

# Evaluate an "Executive VP" role paying 300k vs 150k market average
audit = hr_svc.evaluate_role_productivity(
    heir_id=heir_id,
    role_title="Executive VP of Lifestyle",
    salary=300000.0,
    market_rate_avg=150000.0
)

print(f"Role Status: {audit['status']}")
print(f"Pay Premium: {audit['pay_premium_pct']}% above market")
print(f"Social Maintenance Value: {audit['social_maintenance_value']}")
```

### Applying a Family Discretion Override
```python
from services.hr.heir_governance_svc import HeirGovernanceService

hr_svc = HeirGovernanceService()

# staff_001 achieved 40% on hard math, but principal grants 90% discretion
final_score = hr_svc.apply_discretionary_kpi_override(
    staff_id="HEIR_STAFF_001",
    hard_kpi_score=40.0,
    family_discretion=90.0
)

print(f"Final Governance-Adjusted Score: {final_score}")
```
