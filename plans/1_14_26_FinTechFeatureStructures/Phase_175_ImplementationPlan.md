# Phase 175: MFO 'Best of Both Worlds' Resource Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Family Office Team

---

## 📋 Overview

**Description**: Manage the shared resource pool of a Multi-Family Office. Optimize the utilization of "Shared Services" (Concierge, Private Aviation, Tax Counsel) so that families feel they have dedicated service even while sharing.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 15

---

## 🎯 Sub-Deliverables

### 175.1 Shared Service Ticket System (Concierge) `[ ]`

**Acceptance Criteria**: Helpdesk system for lifestyle requests ("Book jet to Aspen"). Route to shared concierge staff.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE concierge_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL,
    request_type VARCHAR(50),          -- TRAVEL, EVENT, GIFTING
    priority VARCHAR(20),
    status VARCHAR(20),
    
    assigned_to UUID,                  -- Shared Staff ID
    hours_logged DECIMAL(5, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/175_concierge.sql` | `[ ]` |
| Ticket Service | `services/mfo/concierge_service.py` | `[ ]` |

---

### 175.2 Vendor Negotiation Power Aggregator `[ ]`

**Acceptance Criteria**: Aggregate spending power. If 10 families all use NetJets or the same Insurance carrier, negotiate a group discount.

| Component | File Path | Status |
|-----------|-----------|--------|
| Spend Aggregator | `services/mfo/spend_aggregator.py` | `[ ]` |

---

### 175.3 Expert Network Access Graph `[ ]`

**Acceptance Criteria**: Graph of Subject Matter Experts (SMEs). If Family A needs a Cyber Security expert, tap the MFO's vetted network.

| Component | File Path | Status |
|-----------|-----------|--------|
| Expert Graph | `services/neo4j/expert_network.py` | `[ ]` |

---

### 175.4 Family Educational Content Portal `[ ]`

**Acceptance Criteria**: Shared learning generation. "Next Gen" financial literacy courses reused across all families.

| Component | File Path | Status |
|-----------|-----------|--------|
| Content Portal | `services/education/mfo_content.py` | `[ ]` |

---

### 175.5 Institutional Pricing Tier Validator `[ ]`

**Acceptance Criteria**: Verify that the MFO is getting "Institutional" pricing on all funds (lowest expense ratio), confirming the value prop of scale.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Validator | `services/compliance/fee_tier_check.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Concierge Portal | `frontend2/src/components/MFO/ConciergePortal.jsx` | `[ ]` |
| Network Directory | `frontend2/src/components/MFO/ExpertDirectory.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py mfo request <text>` | Create concierge ticket | `[ ]` |
| `python cli.py mfo check-pricing` | Verify institutional fees | `[ ]` |

---

*Last verified: 2026-01-25*
