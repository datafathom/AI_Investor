# Phase 101: Fiduciary-First Entity & Conflict of Interest Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance Team

---

## 📋 Overview

**Description**: Establish core data structures for advisors, prioritizing the high legal standard of Registered Investment Advisors (RIAs) over broker-dealers.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 101.1 Advisor Postgres Table with Fiduciary Status `[ ]`

**Acceptance Criteria**: Implement Postgres table for 'Advisors' with a mandatory 'fiduciary_status' boolean and registration metadata (SEC vs. State).

#### Database Schema

```sql
CREATE TABLE advisors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- Fiduciary Status
    fiduciary_status BOOLEAN NOT NULL DEFAULT FALSE,
    fiduciary_type VARCHAR(50),  -- RIA, BROKER_DEALER, HYBRID
    
    -- Registration
    registration_type VARCHAR(20) NOT NULL,  -- SEC, STATE
    registration_number VARCHAR(50),
    registration_state VARCHAR(2),
    sec_crd_number VARCHAR(20),
    
    -- Firm Details
    firm_name VARCHAR(255),
    firm_type VARCHAR(50),  -- RIA, WIREHOUSE, INDEPENDENT
    
    -- Compliance
    aum_under_management DECIMAL(20, 2),
    fee_structure VARCHAR(50),  -- FEE_ONLY, COMMISSION, HYBRID
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_advisors_fiduciary ON advisors(fiduciary_status);
CREATE INDEX idx_advisors_registration ON advisors(registration_type);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/101_advisors.sql` | `[ ]` |
| Model | `models/advisor.py` | `[ ]` |
| Service | `services/advisor_service.py` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Advisor Model | `tests/unit/test_advisor_model.py` | `[ ]` |
| Integration: Advisor CRUD | `tests/integration/test_advisor_crud.py` | `[ ]` |

---

### 101.2 Conflict of Interest Score (COIS) `[ ]`

**Acceptance Criteria**: Develop a Kafka-driven 'Conflict of Interest Score' (COIS) that aggregates real-time data to flag advisors receiving commissions on recommended products.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| COIS Calculator | `services/compliance/cois_calculator.py` | `[ ]` |
| Commission Detector | `services/compliance/commission_detector.py` | `[ ]` |
| Kafka Consumer | `services/kafka/cois_consumer.py` | `[ ]` |

#### COIS Scoring Logic

| Factor | Weight | Description |
|--------|--------|-------------|
| Commission Revenue | 40% | % of revenue from commissions |
| Product Kickbacks | 30% | Revenue from proprietary products |
| Trading Volume | 15% | Excessive trading patterns |
| Fee Transparency | 15% | Disclosed vs actual fees |

---

### 101.3 Neo4j Advisor Node Separation `[ ]`

**Acceptance Criteria**: Define Neo4j nodes for 'Advisor' types, strictly separating Wealth Managers from pure Asset Managers and Financial Planners.

#### Neo4j Schema

```cypher
// Advisor Node Types
CREATE CONSTRAINT advisor_id IF NOT EXISTS FOR (a:ADVISOR) REQUIRE a.id IS UNIQUE;

// Specialized Sub-types
(:ADVISOR:WEALTH_MANAGER {id, name, fiduciary: true, services: ['TAX', 'ESTATE', 'INSURANCE']})
(:ADVISOR:ASSET_MANAGER {id, name, fiduciary: false, services: ['INVESTMENTS']})
(:ADVISOR:FINANCIAL_PLANNER {id, name, fiduciary: true, services: ['BUDGETING', '529', 'RETIREMENT']})
(:ADVISOR:PRIVATE_BANKER {id, name, net_worth_min: 10000000})

// Relationships
(:ADVISOR)-[:MANAGES]->(CLIENT)
(:ADVISOR)-[:RECOMMENDS {commission_pct: 0.0}]->(PRODUCT)
(:ADVISOR)-[:EMPLOYED_BY]->(FIRM)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Advisor Graph Service | `services/neo4j/advisor_graph.py` | `[ ]` |
| Type Separator | `services/compliance/advisor_type_separator.py` | `[ ]` |

---

### 101.4 Kickback Revenue Validator `[ ]`

**Acceptance Criteria**: Create a validation service that automatically blocks fiduciary nodes from accepting 'kickback' revenue streams.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Kickback Validator | `services/compliance/kickback_validator.py` | `[ ]` |
| Revenue Analyzer | `services/compliance/revenue_analyzer.py` | `[ ]` |

#### Validation Rules

| Rule | Description | Action |
|------|-------------|--------|
| KICKBACK_001 | Fiduciary accepts >5% commission revenue | BLOCK + ALERT |
| KICKBACK_002 | Recommends proprietary products exclusively | WARN |
| KICKBACK_003 | Undisclosed 12b-1 fees | BLOCK + REPORT |

---

### 101.5 AUM Fee Constraint Mapping `[ ]`

**Acceptance Criteria**: Build a relationship mapper in Neo4j to link Advisors to 'Managed Clients' with a standard 1.0% AUM fee constraint for baseline modeling.

#### Neo4j Relationship

```cypher
// Advisor-Client relationship with fee tracking
(:ADVISOR)-[:MANAGES {
    aum_fee_pct: 1.0,
    fee_schedule: 'TIERED',  // FLAT, TIERED, PERFORMANCE
    inception_date: date(),
    billing_frequency: 'QUARTERLY'
}]->(CLIENT)

// Fee tier model
(:ADVISOR)-[:HAS_FEE_SCHEDULE]->(FEE_TIER {
    min_aum: 0,
    max_aum: 1000000,
    fee_pct: 1.0
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Mapper | `services/compliance/fee_mapper.py` | `[ ]` |
| AUM Calculator | `services/aum_calculator.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 101.1 Advisor Table | `[ ]` | `[ ]` |
| 101.2 COIS Calculator | `[ ]` | `[ ]` |
| 101.3 Neo4j Advisor Types | `[ ]` | `[ ]` |
| 101.4 Kickback Validator | `[ ]` | `[ ]` |
| 101.5 AUM Fee Mapping | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py advisor-list` | List all advisors | `[ ]` |
| `python cli.py advisor-cois <id>` | Calculate COIS score | `[ ]` |
| `python cli.py advisor-compliance <id>` | Run compliance check | `[ ]` |

---

## 📦 Dependencies

- Phase 3: TimescaleDB (Postgres schema)
- Phase 4: Neo4j Graph (node structure)

---

*Last verified: 2026-01-25*
