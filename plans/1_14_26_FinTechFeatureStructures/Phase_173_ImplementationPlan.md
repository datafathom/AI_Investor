# Phase 173: Deal Flow Priority & Retail Exclusion Gate

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Market Team

---

## 📋 Overview

**Description**: Manage the scarcity of top-tier private deals. Implement a "Velvet Rope" allocation system. Top clients (SFOs, $50M+) get "First Look" rights. Smaller clients are waitlisted or excluded if the deal is oversubscribed.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 13

---

## 🎯 Sub-Deliverables

### 173.1 Allocation Algorithm (AUM-Weighted) `[ ]`

**Acceptance Criteria**: Allocation logic. If $10M deal is 2x oversubscribed ($20M demand), allocate pro-rata based on Client AUM or "Strategic Value".

#### Backend Implementation

```python
class AllocationEngine:
    """
    Allocate scarce deal capacity.
    """
    def allocat_deal(
        self,
        deal_capacity: Decimal,
        commitments: list[Commitment]
    ) -> AllocationResult:
        # Sort by Priority Tier (SFO > UHNW > HNW)
        # Then Pro-Rata within Tier
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Allocation Engine | `services/deal/allocation_engine.py` | `[ ]` |
| Priority Scorer | `services/crm/client_priority.py` | `[ ]` |

---

### 173.2 Retail "Velvet Rope" Blocking Service `[ ]`

**Acceptance Criteria**: UI/API Logic to hide specific deals from users who don't meet the "Ultra-Accredited" or "Qualified Purchaser" threshold ($5M investments).

| Component | File Path | Status |
|-----------|-----------|--------|
| Access Gate | `services/compliance/velvet_rope.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Locked Deal Card | `frontend2/src/components/Deal/LockedDeal.jsx` | `[ ]` |

---

### 173.3 Postgres Waitlist & "First Look" Timestamping `[ ]`

**Acceptance Criteria**: Strict timestamping of interest ("Soft Circles"). First-Come-First-Serve tied to priority buckets.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE deal_interest_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID NOT NULL,
    user_id UUID NOT NULL,
    committed_amount DECIMAL(20, 2),
    
    -- Priority
    client_tier VARCHAR(20),       -- TIER_1_SFO, TIER_2_UHNW
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    -- Outcome
    allocated_amount DECIMAL(20, 2),
    status VARCHAR(20),            -- WAITLISTED, ALLOCATED, REJECTED
    
    INDEX idx_deal_time (deal_id, timestamp)
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/173_waitlist.sql` | `[ ]` |
| Waitlist Manager | `services/deal/waitlist_manager.py` | `[ ]` |

---

### 173.4 Neo4j Investor Tier Segmentation Node `[ ]`

**Acceptance Criteria**: Graph nodes representing the privilege level of each investor.

```cypher
(:CLIENT)-[:HAS_STATUS]->(:VIP_TIER {
    name: "Strategic Pattern",
    allocation_priority: 1
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tier Graph | `services/neo4j/tier_graph.py` | `[ ]` |

---

### 173.5 Deal Scarcity FOMO Alert `[ ]`

**Acceptance Criteria**: Marketing automation. "Only $2M remaining!" alerts pushed to eligible clients to drive urgency.

| Component | File Path | Status |
|-----------|-----------|--------|
| FOMO Notifier | `services/notifications/fomo_alert.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py deal allocate <id>` | Run allocation algo | `[ ]` |
| `python cli.py deal waitlist` | Show waitlist | `[ ]` |

---

*Last verified: 2026-01-25*
