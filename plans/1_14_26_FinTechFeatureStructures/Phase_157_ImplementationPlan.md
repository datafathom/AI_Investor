# Phase 157: 529 Plan State-Specific Limitation Mapper

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Education Planning Team

---

## 📋 Overview

**Description**: While 529 plans are federal vehicles, their specific investment options, fees, and tax benefits are state-regulated. This phase maps the granular rules for all 50 states to prevent "out-of-state" optimization errors (e.g., suggesting a NY resident use a Utah plan when it costs them a $10k tax deduction).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 17

---

## 🎯 Sub-Deliverables

### 157.1 State-Approved Investment List Table `[ ]`

**Acceptance Criteria**: Database of permitted investment options per state plan. Some states (e.g., prepaid tuition plans) have very restrictive lists.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE state_529_investments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_code VARCHAR(2) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    
    -- Investment Option
    fund_ticker VARCHAR(10),
    fund_name VARCHAR(255),
    asset_class VARCHAR(50),
    expense_ratio DECIMAL(5, 4),
    
    -- Restrictions
    is_open_to_non_residents BOOLEAN,
    min_contribution DECIMAL(10, 2),
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/157_state_investments.sql` | `[ ]` |
| Investment Loader | `services/education/investment_loader.py` | `[ ]` |

---

### 157.2 State Residency Tax Advantaged Recommender `[ ]`

**Acceptance Criteria**: Logic engine: If State X offers tax deduction AND Resident lives in State X -> Recommend State X Plan. If State X has no income tax (e.g., FL, TX) or tax parity (e.g., PA, AZ) -> Recommend Best National Plan (lowest fees).

```python
class PlanRecommender:
    def recommend_plan(self, residence_state: str) -> RecommendedPlan:
        state_rules = self.get_state_rules(residence_state)
        
        if state_rules.has_income_tax and state_rules.has_in_state_deduction:
            return self.get_in_state_plan(residence_state)
        elif state_rules.has_tax_parity:
            return self.get_best_national_plan() # Use curated low-fee list
        else:
            return self.get_best_national_plan()
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Recommender Engine | `services/education/plan_recommender.py` | `[ ]` |
| State Rules Config | `config/state_529_rules.json` | `[ ]` |

---

### 157.3 Neo4j Beneficiary Age → Glide-Path Relationship `[ ]`

**Acceptance Criteria**: Graph logic to enforce state-specific "Age-Based Portfolio" rules. Some states force you into their predefined glide paths.

```cypher
(:BENEFICIARY {age: 14})-[:ENROLLED_IN]->(:PLAN:NY_529)
(:PLAN:NY_529)-[:OFFERS]->(:PORTFOLIO:AGE_BASED_14_16)
(:PORTFOLIO:AGE_BASED_14_16)-[:ALLOCATION]->(:ASSET_MIX {equity: 0.50, bond: 0.50})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| State Graph Service | `services/neo4j/state_529_graph.py` | `[ ]` |

---

### 157.4 Kafka Over-Funding Risk Flag `[ ]`

**Acceptance Criteria**: Check against "Maximum Aggregate Limit" per beneficiary (varies by state, usually ~$350k-$550k). Contributions above this are rejected to avoid penalties.

| Component | File Path | Status |
|-----------|-----------|--------|
| Limit Monitor | `services/kafka/limit_monitor.py` | `[ ]` |
| Alert Service | `services/alerts/overfunding_alert.py` | `[ ]` |

---

### 157.5 Qualified Expense Logic Validator `[ ]`

**Acceptance Criteria**: Verify state conformity to federal "Qualified Expenses". Some states do NOT conform to the federal expansion for K-12 tuition or Student Loan repayment (meaning it's taxable at the state level).

| Component | File Path | Status |
|-----------|-----------|--------|
| Non-Conformity Check | `services/tax/state_conformity.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 529 recommend <state>` | Get plan recommendation | `[ ]` |
| `python cli.py 529 check-limit <state>` | Check contrib limit | `[ ]` |

---

*Last verified: 2026-01-25*
