# Phase 170: Descendant Employment & Discretionary Override

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: HR & Governance Team

---

## 📋 Overview

**Description**: Manage family member employment within the Family Office or Family Business. Balances "Meritocracy" (qualified for the job) vs. "Nepotism" (creating a role for an heir). Handles discretionary compensation overrides (paying a child more than market rate) while flagging tax implications (Gift disguised as Salary).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 10

---

## 🎯 Sub-Deliverables

### 170.1 Neo4j Descendant Employee Nodes `[ ]`

**Acceptance Criteria**: Map family members who are also employees. Distinguish them from non-family staff.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:PERSON:FAMILY_MEMBER {name: "Heir"})-[:EMPLOYED_AS {
    title: "VP of Special Projects",
    start_date: date(),
    is_nepotism_role: true
}]->(:FAMILY_BUSINESS)

(:PERSON:NON_FAMILY {name: "Professional"})-[:EMPLOYED_AS {
    title: "CFO",
    is_nepotism_role: false
}]->(:FAMILY_BUSINESS)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Employment Graph | `services/neo4j/employment_graph.py` | `[ ]` |

---

### 170.2 'Cushy Job' Low-Demand Role Flag `[ ]`

**Acceptance Criteria**: Flag roles with high salary but low KPI requirements. This helps the Family Council monitor "freeloading" vs. productive work.

| Component | File Path | Status |
|-----------|-----------|--------|
| Role Evaluator | `services/hr/role_evaluator.py` | `[ ]` |

---

### 170.3 Postgres Discretionary KPI Override for Heirs `[ ]`

**Acceptance Criteria**: Allow "Soft KPIs" for heirs (e.g., "Attend Board Meetings") vs. "Hard KPIs" for pros (e.g., "Grow Revenue 10%").

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE kpi_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id UUID NOT NULL,
    year INTEGER NOT NULL,
    
    -- Goal
    kpi_description TEXT,
    target_metric DECIMAL(10, 2),
    actual_metric DECIMAL(10, 2),
    
    -- Evaluation
    is_discretionary_override BOOLEAN,  -- True if "Nice try, here's the bonus anyway"
    override_reason TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/170_kpi_override.sql` | `[ ]` |
| KPI Manager | `services/hr/kpi_manager.py` | `[ ]` |

---

### 170.4 Employment Outlet Productivity Model `[ ]`

**Acceptance Criteria**: Model the "Social Value" of employment. Even if an heir is not efficient, employment provides structure and purpose (Social Class Maintenance), preventing "Trust Fund Baby" syndrome.

| Component | File Path | Status |
|-----------|-----------|--------|
| Productivity Model | `services/analysis/productivity_model.py` | `[ ]` |

---

### 170.5 Social Perception vs. Actual Productivity Mapping `[ ]`

**Acceptance Criteria**: A "Gap Analysis" graph. How the public perceives the heir's role vs. internal productivity data.

| Component | File Path | Status |
|-----------|-----------|--------|
| Perception Mapper | `services/reporting/perception_gap.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Governance Dashboard | `frontend2/src/components/SFO/GovernanceDash.jsx` | `[ ]` |
| Family HR Review | `frontend2/src/components/HR/FamilyReview.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py governance list-heirs` | Show employed family | `[ ]` |
| `python cli.py governance audit-kpi` | Check overrides | `[ ]` |

---

*Last verified: 2026-01-25*
