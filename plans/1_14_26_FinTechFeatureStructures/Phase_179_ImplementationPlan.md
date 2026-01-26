# Phase 179: Deal Flow Network & Network Access Perk

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Market Team

---

## 📋 Overview

**Description**: Systematize the "Network Effect" of UHNW clients. "Who knows who?" Leverage the collective network of the Family Office to get access to exclusive deals, boards, and experts.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 19

---

## 🎯 Sub-Deliverables

### 179.1 Rolodex & CRM Integration (Salesforce API) `[ ]`

**Acceptance Criteria**: Centralized CRM for the Family Office. Sync contacts from email/Outlook/Salesforce. Tag "Deal Sources" and "Industry Experts".

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE network_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    organization VARCHAR(100),
    role VARCHAR(50),
    
    -- Network Value
    deal_source_score INTEGER,         -- 1-10 (Good source of deals?)
    expert_domain VARCHAR(50),         -- ENERGY, TECH, REAL_ESTATE
    relationship_strength INTEGER,     -- 1-5 (How well do we know them?)
    
    owner_id UUID,                     -- Who owns this relationship?
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/179_network_crm.sql` | `[ ]` |
| CRM Integrator | `services/external/salesforce_adapter.py` | `[ ]` |

---

### 179.2 Neo4j "Who Knows Who" Pathfinding `[ ]`

**Acceptance Criteria**: Shortest path algorithms. "We want to invest in SpaceX. Who do we know that knows Elon Musk?"

```cypher
MATCH (us:FAMILY_OFFICE), (target:PERSON {name: "Elon Musk"}),
p = shortestPath((us)-[:KNOWS*..3]-(target))
RETURN p
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Pathfinding Service | `services/neo4j/pathfinder.py` | `[ ]` |

---

### 179.3 Deal Source Attribution Tracking `[ ]`

**Acceptance Criteria**: Track where the best deals come from. If "Goldman Sachs" sends us 10 bad deals and "Friend Bob" sends 1 unicorn, prioritize Bob.

| Component | File Path | Status |
|-----------|-----------|--------|
| Attribution Engine | `services/analysis/deal_source_quality.py` | `[ ]` |

---

### 179.4 "Club Deal" Formation Tool `[ ]`

**Acceptance Criteria**: Tool to spin up a "Club Deal". We found a $50M deal, we take $10M, we need to syndicate $40M to our network. Automate the invites and teases.

| Component | File Path | Status |
|-----------|-----------|--------|
| Club Deal Manager | `services/deal/club_deal_manager.py` | `[ ]` |

---

### 179.5 Event & Conference ROI Tracker `[ ]`

**Acceptance Criteria**: Did attending "Davos" or "Milken" generate any value? Track events against resulting contacts and deals.

| Component | File Path | Status |
|-----------|-----------|--------|
| Event ROI Tracker | `services/analysis/event_roi.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Network Visualizer | `frontend2/src/components/Network/NetworkGraph.jsx` | `[ ]` |
| CRM Dashboard | `frontend2/src/components/CRM/ContactList.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py network find-path <target>` | Find connection | `[ ]` |
| `python cli.py deal spin-up-club` | Create club deal | `[ ]` |

---

*Last verified: 2026-01-25*
