# Phase 155: Heir Litigation & Family Conflict Risk Mapper

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Estate Planning & Legal Team

---

## 📋 Overview

**Description**: Using a "Pre-Mortem" analysis to predict and prevent family litigation. Identify potential conflict points (e.g., unequal distributions, step-children vs. biological children, ambiguous personal property) and implement legal/technical guardrails to minimize the risk of a Will contest.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 15

---

## 🎯 Sub-Deliverables

### 155.1 Family Conflict Score `[ ]`

**Acceptance Criteria**: Algorithm that assigns a "Litigation Risk Score" (0-100) based on family dynamics data points. High scores trigger automated recommendations for "In Terrorem" (No-Contest) clauses and professional trustees.

#### Backend Implementation

```python
class ConflictAssessor:
    """
    Assess the probability of estate litigation.
    
    Risk Factors:
    - Multiple marriages (Blended Family risk).
    - Unequal distributions (>10% variance).
    - History of substance abuse or financial instability in heirs.
    - Estranged family members.
    - Large illiquid assets (Vacation home, Family business).
    """
    
    def calculate_litigation_risk(self, family_tree: FamilyTree, distribution_plan: Plan) -> RiskAssessment:
        risk_score = 0
        
        # Blended Family Logic
        if family_tree.has_step_children and family_tree.has_biological_children:
            risk_score += 25
            
        # Unequal Logic
        if self._is_unequal_distribution(distribution_plan):
            risk_score += 20
            
        return RiskAssessment(score=risk_score, recommendations=self._get_mitigation_strategies(risk_score))
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Conflict Assessor | `services/estate/conflict_assessor.py` | `[ ]` |
| Risk Model | `models/risk/litigation_risk.py` | `[ ]` |

---

### 155.2 Neo4j Litigant Heir → Trust Friction Mapping `[ ]`

**Acceptance Criteria**: Graph modeling of "Friction Points" where specific beneficiaries have competing interests in the same asset (e.g., Sibling A wants to keep the house, Sibling B wants to sell it).

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:PERSON:HEIR {name: "Sibling A"})-[:DESIRES {action: "KEEP"}]->(:ASSET:REAL_ESTATE)
(:PERSON:HEIR {name: "Sibling B"})-[:DESIRES {action: "SELL"}]->(:ASSET:REAL_ESTATE)

// Friction Detection Query
MATCH (p1:HEIR)-[d1:DESIRES]->(a:ASSET)<-[d2:DESIRES]-(p2:HEIR)
WHERE d1.action <> d2.action
RETURN a, p1, p2, "High Conflict Risk" as status
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Friction Graph | `services/neo4j/friction_graph.py` | `[ ]` |

---

### 155.3 Well-Defined Wills Prioritization Logic `[ ]`

**Acceptance Criteria**: System to verify that "Specific Bequests" (e.g., "I leave my 1969 Camaro to John") take priority over "Residual Bequests" (e.g., "I leave the rest to Jane") in the programmatic distribution logic.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bequest Prioritizer | `services/estate/bequest_prioritizer.py` | `[ ]` |

---

### 155.4 Postgres Fairness Dispute Mediation Log `[ ]`

**Acceptance Criteria**: Immutable log of pre-death "Family Meetings" or mediation sessions where the plan was explained. This serves as evidence of the Grantor's intent and capacity if challenged later.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE mediation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estate_plan_id UUID NOT NULL,
    session_date TIMESTAMPTZ NOT NULL,
    
    -- Attendees
    attendees JSONB,                   -- ["Grantor", "Heir A", "Attorney"]
    
    -- Evidence
    recording_url VARCHAR(255),        -- S3 link to video/audio
    transcript_text TEXT,
    
    -- Outcome
    topics_discussed TEXT,
    consensus_reached BOOLEAN,
    signed_waiver_received BOOLEAN,    -- Estoppel Key
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/155_mediation_log.sql` | `[ ]` |
| Evidence Locker | `services/compliance/evidence_locker.py` | `[ ]` |

---

### 155.5 Asset Liquidation Protocol for Disagreements `[ ]`

**Acceptance Criteria**: Automatic "Tie-Breaker" logic embedded in the trust. If heirs cannot agree on asset disposition within X days, the Trustee is *compelled* to liquidate the asset and distribute cash (removing the fight).

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidation Protocol | `services/estate/liquidation_enforcer.py` | `[ ]` |
| Tie Breaker Timer | `services/estate/tie_breaker.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py estate assess-conflict` | Calculate risk score | `[ ]` |
| `python cli.py estate find-friction` | Query Neo4j conflicts | `[ ]` |

---

*Last verified: 2026-01-25*
