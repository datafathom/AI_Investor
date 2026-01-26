# Phase 178: SFO Long-Term Multi-Generational Mandate

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Family Office Team

---

## 📋 Overview

**Description**: Encodify the "100-Year Plan". Move the investment horizon from "Quarterly" to "Generational". Shift focus from short-term volatility to long-term compounding, capital preservation, and inflation protection.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 18

---

## 🎯 Sub-Deliverables

### 178.1 "100-Year Portfolio" Asset Allocation Model `[ ]`

**Acceptance Criteria**: Implement an endowment-style model (Yale Model). High allocation to illiquids, equities, and real assets. Zero concern for weekly liquidity.

```python
class EndowmentModel:
    """
    Generate asset allocation for infinite time horizon.
    """
    def generate_allocation(self) -> Allocation:
        return Allocation(
            public_equity=0.30,
            private_equity=0.30,
            real_estate=0.20,
            absolute_return=0.15,
            cash_bonds=0.05
        )
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Allocation Engine | `services/portfolio/endowment_model.py` | `[ ]` |

---

### 178.2 Inflation-Adjusted Principal Protection Gate `[ ]`

**Acceptance Criteria**: Spending rule. Determine that the family can only spend "Real Returns" (Nominal - Inflation). If inflation is 5% and return is 6%, only 1% is spendable to preserve principal.

| Component | File Path | Status |
|-----------|-----------|--------|
| Spending Rule | `services/planning/spending_rule.py` | `[ ]` |

---

### 178.3 Family Governance & Constitution Viewer `[ ]`

**Acceptance Criteria**: Digital Family Constitution. Store the "Values" and "Mission" of the family to guide future generations.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE family_constitution (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL,
    sections JSONB,                    -- {"Mission": "...", "Values": "..."}
    last_ratified_date DATE,
    ratified_by UUID[],                -- Array of Family Member IDs
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/178_constitution.sql` | `[ ]` |
| Governance Svc | `services/sfo/governance.py` | `[ ]` |

---

### 178.4 Next-Gen Education Curriculum Tracker `[ ]`

**Acceptance Criteria**: Learning Management System (LMS) for heirs. Track progress in "Financial Literacy 101", "Philanthropy", "Board Governance".

| Component | File Path | Status |
|-----------|-----------|--------|
| LMS Service | `services/education/heir_lms.py` | `[ ]` |

---

### 178.5 Philanthropic Legacy Simulator `[ ]`

**Acceptance Criteria**: Model the impact of charitable giving over 100 years. "Endowed Chair at University" vs. "Private Foundation Spend-Down".

| Component | File Path | Status |
|-----------|-----------|--------|
| Philanthropy Sim | `services/simulation/philanthropy_sim.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Legacy Dashboard | `frontend2/src/components/SFO/LegacyDashboard.jsx` | `[ ]` |
| Constitution View | `frontend2/src/components/SFO/ConstitutionViewer.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sfo calc-spending` | Calculate safe spend | `[ ]` |
| `python cli.py sfo audit-governance` | Check ratification | `[ ]` |

---

*Last verified: 2026-01-25*
