# Phase 118: Defined Benefit Sustainability Simulator

> **Status**: `[ ]` Not Started | **Owner**: Retirement Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Phase 18

## 📋 Overview
**Description**: Simulate the sustainability of defined benefit pension plans, modeling employer solvency, funding ratios, and conversion to defined contribution alternatives.

---

## 🎯 Sub-Deliverables

### 118.1 Pension Sustainability Simulation `[ ]`
| Component | File Path | Status |
|-----------|-----------|--------|
| Pension Simulator | `services/retirement/pension_simulator.py` | `[ ]` |
| Funding Ratio Analyzer | `services/retirement/funding_ratio.py` | `[ ]` |

### 118.2 Legacy Pension Payment Schedule Table `[ ]`
```sql
CREATE TABLE pension_schedules (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    pension_provider VARCHAR(255),
    monthly_benefit DECIMAL(20, 2),
    payment_start_date DATE,
    cola_adjustment DECIMAL(5, 4),
    survivor_benefit_pct DECIMAL(5, 4),
    funding_ratio DECIMAL(5, 4),
    employer_credit_rating VARCHAR(10)
);
```

### 118.3 Employer to Matching Migration Tool `[ ]`
| Component | File Path | Status |
|-----------|-----------|--------|
| Migration Calculator | `services/retirement/db_to_dc_migration.py` | `[ ]` |

### 118.4 Pension Failure Historical Database `[ ]`
Track historical pension failures for risk modeling.

### 118.5 Grandfathered Pension Fixed-Income Logic `[ ]`
Treat pension income as bond-like fixed income in portfolio allocation.

---

## 📊 Phase Status: `[ ]` NOT STARTED
