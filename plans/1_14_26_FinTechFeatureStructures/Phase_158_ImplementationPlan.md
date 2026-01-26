# Phase 158: Fiduciary Standard Compliance Audit Log

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance Team

---

## 📋 Overview

**Description**: Create an immutable "Fiduciary Audit Trail". Every recommendation made by the AI or Advisor must include a "Best Interest Justification" recorded in the database. This defends against Regulation Best Interest (Reg BI) and DOL Fiduciary Rule audits.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 18

---

## 🎯 Sub-Deliverables

### 158.1 Postgres Trade Best Interest Justification Log `[ ]`

**Acceptance Criteria**: Every trade order or plan recommendation *must* be linked to a structured justification record (Why this? Why now? Why better than the alternative?).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE fiduciary_justifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_id UUID NOT NULL,
    client_id UUID NOT NULL,
    advisor_id UUID NOT NULL, -- or AI_AGENT_ID
    
    -- The "Why"
    rationale_code VARCHAR(50),        -- REBALANCE, TAX_LOSS, RISK_REDUCTION, LOWER_COST
    rationale_text TEXT NOT NULL,
    
    -- Comparison
    considered_alternatives JSONB,     -- ["Ticker A", "Ticker B"]
    cost_comparison_result VARCHAR(20), -- LOWER_COST, HIGHER_PERFORMANCE, BETTER_FIT
    
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    is_immutable BOOLEAN DEFAULT TRUE
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/158_justification_log.sql` | `[ ]` |
| Justification Service | `services/compliance/justification_service.py` | `[ ]` |

---

### 158.2 Kafka Conflict of Interest Consumer `[ ]`

**Acceptance Criteria**: Real-time scanner for conflicts (e.g., Advisor recommending a proprietary fund where they get a kickback). If detected, it must be flagged and disclosed immediately.

| Component | File Path | Status |
|-----------|-----------|--------|
| Conflict Scanner | `services/kafka/conflict_scanner.py` | `[ ]` |
| Disclosure Trigger | `services/compliance/disclosure_trigger.py` | `[ ]` |

---

### 158.3 Neo4j Fee Disclosure Graph `[ ]`

**Acceptance Criteria**: Graph visualizer showing exactly where fees are going (Advisor, Platform, Fund Manager, 12b-1) to ensure total transparency.

```cypher
(:CLIENT)-[:PAYS_FEE {amount: 250}]->(:FEE_POT)
(:FEE_POT)-[:DISTRIBUTED_TO]->(:PLATFORM {amount: 25})
(:FEE_POT)-[:DISTRIBUTED_TO]->(:ADVISOR {amount: 200})
(:FEE_POT)-[:DISTRIBUTED_TO]->(:ETF_MANAGER {amount: 25})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Graph Service | `services/neo4j/fee_graph.py` | `[ ]` |

---

### 158.4 AUM vs. Performance Fee Comparison Logic `[ ]`

**Acceptance Criteria**: Logic to determine if the fee structure chosen (AUM % vs. Performance Fee) is actually in the client's best interest based on volatility and expected returns.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Analysis Engine | `services/analysis/fee_analysis.py` | `[ ]` |

---

### 158.5 Annual Fiduciary Compliance Report Generator `[ ]`

**Acceptance Criteria**: Automated PDF generation of the "Annual Best Interest Review" required for compliance files.

| Component | File Path | Status |
|-----------|-----------|--------|
| Report Generator | `services/reporting/compliance_pdf.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Compliance Dashboard | `frontend2/src/components/Admin/ComplianceDash.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py compliance log-justification` | Rec justification | `[ ]` |
| `python cli.py compliance generate-report` | Annual Review PDF | `[ ]` |

---

*Last verified: 2026-01-25*
