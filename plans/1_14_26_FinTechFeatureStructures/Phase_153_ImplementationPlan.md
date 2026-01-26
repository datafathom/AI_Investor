# Phase 153: Testamentary Trust Activation Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Estate Planning Team

---

## 📋 Overview

**Description**: Automate the creation/funding of "Testamentary Trusts" which spring into existence *only upon death* via the Will. Used for minor children or contingent beneficiaries to prevent outright inheritance at age 18.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 13

---

## 🎯 Sub-Deliverables

### 153.1 Death Certificate Kafka Trigger `[ ]`

**Acceptance Criteria**: Trigger the estate settlement workflow upon verified input of a death certificate signal.

#### Kafka Topic

```json
{
    "topic": "client-life-events",
    "schema": {
        "event_type": "DEATH_VERIFIED",
        "user_id": "uuid",
        "date_of_death": "date",
        "verified_by": "executor_id"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Death Handler | `services/kafka/death_handler.py` | `[ ]` |
| Workflow Initiator | `services/estate/settlement_workflow.py` | `[ ]` |

---

### 153.2 Postgres Will-Based Trust Instructions Schema `[ ]`

**Acceptance Criteria**: Store the "Pour-Over" instructions. Assets not already in trust are "poured over" into the Testamentary Trust schema.

#### Postgres Schema

```sql
CREATE TABLE testamentary_instructions (
    id UUID PRIMARY KEY,
    will_id UUID NOT NULL,
    
    -- Creation Triggers
    trigger_condition VARCHAR(100),    -- IF_SPOUSE_PREDECEASED
    trust_name VARCHAR(100),           -- "Children's Trust"
    
    -- Terms
    trustee_id UUID,
    distribution_ages JSONB,           -- {25: 0.33, 30: 0.33, 35: 0.34}
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Instruction Parser | `services/estate/instruction_parser.py` | `[ ]` |

---

### 153.3 Neo4j Individual → Post-Mortem Trust Transition `[ ]`

**Acceptance Criteria**: Graph operation to re-parent assets from the deceased User node to the newly created Trust node.

```cypher
MATCH (u:PERSON {is_deceased: true})
MATCH (u)-[:OWNS]->(a:ASSET)
CREATE (t:TRUST:TESTAMENTARY {name: "Child Trust"})
CREATE (t)-[:OWNS]->(a)
DELETE (u)-[:OWNS]->(a)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Asset Re-Parenting | `services/neo4j/reparent_assets.py` | `[ ]` |

---

### 153.4 Estate Residue Funding Service `[ ]`

**Acceptance Criteria**: Logic to sweep "Residue" (everything left over after specific bequests) into the trust.

| Component | File Path | Status |
|-----------|-----------|--------|
| Residue Sweeper | `services/estate/residue_sweeper.py` | `[ ]` |

---

### 153.5 Executor Authorization Verification `[ ]`

**Acceptance Criteria**: Verify the Executor/Personal Representative has Court Letters Testamentary before allowing them access to move assets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Auth Verifier | `services/compliance/executor_auth.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py estate trigger-death` | Dev sim of death event | `[ ]` |
| `python cli.py estate pour-over` | Execute pour-over logic | `[ ]` |

---

*Last verified: 2026-01-25*
