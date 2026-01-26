# Phase 161: Single Family Office (SFO) Economy of Scale Model

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Family Office Team

---

## 📋 Overview

**Description**: Create a model to justify the creation of a Single Family Office (SFO). Analyze the "Breakeven Point" (usually >$100M AUM) where the cost of in-house staff (CIO, CFO, Analysts) becomes cheaper than paying 1% AUM fees to external advisors.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 1

---

## 🎯 Sub-Deliverables

### 161.1 Postgres SFO Operating Expense Table ($500k CIO, $200k Analyst, $30k Bloomberg) `[ ]`

**Acceptance Criteria**: Detailed tracking of SFO operating budget. Staff compensation, technology costs (Bloomberg Terminal), legal retainers, and office overhead.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE sfo_operating_budget (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id UUID NOT NULL,
    fiscal_year INTEGER NOT NULL,
    
    -- Staff Compensation
    role_title VARCHAR(50),            -- CIO, CFO, ANALYST
    base_salary DECIMAL(20, 2),
    target_bonus DECIMAL(20, 2),
    benefits_cost DECIMAL(20, 2),
    
    -- Technology & Ops
    technology_fees DECIMAL(20, 2),    -- Bloomberg, Addepar
    office_rent DECIMAL(20, 2),
    legal_retainer DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/161_sfo_budget.sql` | `[ ]` |
| Budget Planner | `services/sfo/budget_planner.py` | `[ ]` |

---

### 161.2 Net Worth Justification Engine (>$100M) `[ ]`

**Acceptance Criteria**: Engine that calculates the "Fee Hurdle". If Wealth = $500M, a 1% fee is $5M/year. An SFO might cost $2M/year. Saving = $3M. Implementation justified.

```python
class SFOJustificationEngine:
    """
    Compare External RIA Fees vs. SFO Operating Costs.
    """
    def generate_analysis(
        self,
        aum: Decimal,
        external_fee_rate: Decimal = 0.01
    ) -> AnalysisResult:
        external_cost = aum * external_fee_rate
        in_house_cost = self._estimate_sfo_budget(aum)
        
        breakeven = external_cost > in_house_cost
        savings = external_cost - in_house_cost
        
        return AnalysisResult(justified=breakeven, annual_savings=savings)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Justification Engine | `services/sfo/justification_engine.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Breakeven Calculator | `frontend2/src/components/SFO/BreakevenCalc.jsx` | `[ ]` |

---

### 161.3 1% Advisor Fee vs. $1M SFO Budget Comparison `[ ]`

**Acceptance Criteria**: Visualization comparing the linear growth of AUM fees vs. the step-function cost of SFO staffing.

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparison Chart | `frontend2/src/components/Charts/FeeVsCost.jsx` | `[ ]` |

---

### 161.4 Neo4j Investment Staff Compensation Tracking `[ ]`

**Acceptance Criteria**: Graph relationship mapping staff incentives (Carry, Bonus) to investment performance, aligning interests.

```cypher
(:STAFF:CIO {name: "Chief Investment Officer"})-[:EARNS_PERFORMANCE_BONUS {
    hurdle_rate: 0.08,
    bonus_pool_pct: 0.10
}]->(:PORTFOLIO)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Comp Graph Service | `services/neo4j/sfo_comp_graph.py` | `[ ]` |

---

### 161.5 'Headache Factor' Stress Model `[ ]`

**Acceptance Criteria**: Quantify the non-financial cost of managing staff (HR issues, turnover). Is the savings worth the headache?

| Component | File Path | Status |
|-----------|-----------|--------|
| Complexity Scorer | `services/sfo/complexity_scorer.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sfo analyze <aum>` | Run justification analysis | `[ ]` |
| `python cli.py sfo budget-template` | Generate sample budget | `[ ]` |

---

*Last verified: 2026-01-25*
