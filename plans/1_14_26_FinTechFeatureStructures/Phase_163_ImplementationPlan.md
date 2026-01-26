# Phase 163: Family Office CIO & Professional Comp Tracker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: HR & Talent Team

---

## 📋 Overview

**Description**: Manage the compensation, performance, and productivity of high-cost Family Office staff. Track base salary, performance bonuses (benchmarked to Portfolio Alpha), and carried interest participation (phantom equity) to ensure alignment with the family's long-term goals.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 3

---

## 🎯 Sub-Deliverables

### 163.1 Postgres CIO Base + Bonus Range Log ($400-500k) `[ ]`

**Acceptance Criteria**: Database for compensation benchmarking. Store industry averages to ensure the SFO is paying competitive rates to retain top talent.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE staff_compensation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    role_type VARCHAR(50),             -- CIO, PM, ANALYST, CONTROLLER
    
    -- Current Comp
    base_salary DECIMAL(20, 2),
    bonus_structure_json JSONB,        -- {"hurdle": 0.05, "percent": 0.10, "cap": 500000}
    carry_points_bps INTEGER,          -- e.g. 500 bps = 5% of carry pool
    
    -- Benchmarks
    industry_avg_base DECIMAL(20, 2),
    industry_avg_total DECIMAL(20, 2),
    last_benchmarked_date DATE,
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/163_staff_comp.sql` | `[ ]` |
| Compensation Manager | `services/hr/comp_manager.py` | `[ ]` |

---

### 163.2 Back Office Outsourcing Cost Service `[ ]`

**Acceptance Criteria**: Calculator to decide "Build vs. Buy" for back-office functions. Compare cost of hiring a full-time Controller vs. outsourcing to a Fund Admin/CPA firm.

```python
class OutsourceCalculator:
    """
    Compare In-House vs. Outsourced costs.
    """
    def compare_costs(self, function: str, transaction_volume: int) -> Comparison:
        in_house_est = self.estimate_hiring_cost(function)
        outsourced_est = self.estimate_vendor_cost(function, transaction_volume)
        return Comparison(in_house=in_house_est, outsourced=outsourced_est)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Outsource Calculator | `services/operations/outsource_calc.py` | `[ ]` |

---

### 163.3 Kafka Trading Technology Expense Stream `[ ]`

**Acceptance Criteria**: Track "Seat Costs" for expensive tech (Bloomberg Terminal @ $2,500/mo, FactSet). Stream usage logs via Kafka to identify unused licenses that can be cut.

#### Kafka Topic

```json
{
    "topic": "tech-usage-logs",
    "schema": {
        "user_id": "uuid",
        "tool_name": "string",
        "session_duration_min": "integer",
        "features_accessed": ["NEWS", "CHARTING", "TRADING"],
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Usage Monitor | `services/kafka/tech_usage_monitor.py` | `[ ]` |
| Cost Optimizer | `services/operations/tech_cost_opt.py` | `[ ]` |

---

### 163.4 Staff Productivity Metric (Portfolio Alpha) `[ ]`

**Acceptance Criteria**: Attribute Portfolio Alpha to specific Investment Staff. Did the CIO's asset allocation decisions add value? Did the Analyst's stock picks outperform?

| Component | File Path | Status |
|-----------|-----------|--------|
| Attribution Engine | `services/performance/staff_attribution.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Staff Assessment | `frontend2/src/components/HR/StaffPerformance.jsx` | `[ ]` |

---

### 163.5 Due Diligence Travel Budget Tracker `[ ]`

**Acceptance Criteria**: Expense tracker for due diligence trips (visiting factories, meeting hedge fund managers). Correlate travel spend with investment outcomes (ROI on Due Diligence).

| Component | File Path | Status |
|-----------|-----------|--------|
| Expense Tracker | `services/operations/travel_expense.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py hr check-comp <role>` | Show market rate | `[ ]` |
| `python cli.py hr calc-bonus <id>` | Calculate EOY bonus | `[ ]` |

---

*Last verified: 2026-01-25*
