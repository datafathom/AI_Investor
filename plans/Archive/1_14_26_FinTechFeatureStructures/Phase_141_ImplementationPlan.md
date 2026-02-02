# Phase 141: Neo4j Trust Hierarchy & Relationship Mapper

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Legal & Estate Processing Team

---

## 📋 Overview

**Description**: Map complex trust hierarchies in Neo4j, defining the relationships between Grantors (creators), Trustees (managers), and Beneficiaries (recipients). Differentiate between Revocable (Grantor control) and Irrevocable (Tax shield) structures.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 1

---

## 🎯 Sub-Deliverables

### 141.1 Grantor/Trustee/Beneficiary Node Definitions `[ ]`

**Acceptance Criteria**: Define standard Neo4j nodes for all parties involved in a trust relationship.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
// Trust Node
(:TRUST {
    id: "uuid",
    name: "The Smith Family Trust",
    type: "REVOCABLE",          // REVOCABLE, IRREVOCABLE, TESTAMENTARY
    tax_id: "XX-XXXXXXX",
    date_established: date()
})

// Role Nodes
(:PERSON {name: "John Smith"})-[:IS_GRANTOR_OF]->(:TRUST)
(:PERSON {name: "Jane Smith"})-[:IS_TRUSTEE_OF {
    type: "PRIMARY",            // PRIMARY, SUCCESSOR, CO-TRUSTEE
    powers: ["INVEST", "DISTRIBUTE", "SELL"]
}]->(:TRUST)
(:PERSON {name: "Baby Smith"})-[:IS_BENEFICIARY_OF {
    type: "CURRENT",            // CURRENT, REMAINDER
    percentage: 0.50
}]->(:TRUST)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Trust Graph Service | `services/neo4j/trust_graph.py` | `[ ]` |
| Role Manager | `services/estate/role_manager.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Trust Visualizer | `frontend2/src/components/Neo4j/TrustVisualizer.jsx` | `[ ]` |
| Role Editor | `frontend2/src/components/Estate/RoleEditor.jsx` | `[ ]` |

---

### 141.2 OWNS_ASSETS Trust → Portfolio Relationship `[ ]`

**Acceptance Criteria**: Properly model the legal ownership of assets by the Trust entity rather than the individual persons.

#### Neo4j Schema

```cypher
(:TRUST)-[:OWNS_ASSETS {
    titling_status: "VERIFIED",
    custodian_account: "XXXX-5678"
}]->(:PORTFOLIO)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Ownership Service | `services/estate/ownership_service.py` | `[ ]` |

---

### 141.3 Human vs. Legal Entity Ownership Logic `[ ]`

**Acceptance Criteria**: Logic to distinguish between assets owned by a specific human (Individual Account) and assets owned by an entity (Trust/LLC).

```python
class OwnershipResolver:
    """
    Resolve legal owner of assets.
    
    Logic:
    - If account type == TRUST, owner is Trust Entity.
    - If account type == INDIVIDUAL, owner is Person.
    - Grantor of Revocable Trust is tax owner (pass-through).
    - Irrevocable Trust is separate tax entity.
    """
    
    def resolve_tax_owner(self, asset_id: UUID) -> LegalEntity:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Ownership Resolver | `services/legal/ownership_resolver.py` | `[ ]` |

---

### 141.4 Postgres Trust Stipulations Schema `[ ]`

**Acceptance Criteria**: Store specific text stipulations and clauses from the trust document (e.g., "Distribute income quarterl", "Principal for health/education only").

#### Postgres Schema

```sql
CREATE TABLE trust_stipulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    clause_type VARCHAR(50) NOT NULL,      -- DISTRIBUTION, INVESTMENT, SUCCESSION
    description TEXT NOT NULL,
    
    -- Logic triggers
    trigger_condition VARCHAR(100),        -- AGE > 25, MARRIAGE, GRADUATION
    enforcement_level VARCHAR(20),         -- STRICT, DISCRETIONARY
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/141_trust_stipulations.sql` | `[ ]` |
| Stipulation Service | `services/estate/stipulation_service.py` | `[ ]` |

---

### 141.5 Successor Trustee Graph Mapping `[ ]`

**Acceptance Criteria**: Map the chain of succession for trustees in Neo4j to handle "what-if" scenarios (e.g., if Primary Trustee dies, Successor 1 takes over).

```cypher
(:PERSON:TRUSTEE)-[:SUCCEEDED_BY {order: 1}]->(:PERSON:SUCCESSOR_1)
(:PERSON:SUCCESSOR_1)-[:SUCCEEDED_BY {order: 2}]->(:PERSON:SUCCESSOR_2)
(:PERSON:SUCCESSOR_2)-[:SUCCEEDED_BY {order: 3}]->(:INSTITUTION:CORP_TRUSTEE)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Succession Mapper | `services/neo4j/succession_mapper.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py trust graph <id>` | Show trust hierarchy | `[ ]` |
| `python cli.py trust verify-owner` | Verify asset ownership | `[ ]` |

---

*Last verified: 2026-01-25*
