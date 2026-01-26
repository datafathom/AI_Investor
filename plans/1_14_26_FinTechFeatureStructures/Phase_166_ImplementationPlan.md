# Phase 166: Syndication Network & Email List Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Private Market Team

---

## 📋 Overview

**Description**: Build a platform for "Syndications". Unlike funds, syndications allow investors to pick specific deals (e.g., "Main Street Apartments"). Manage the email distribution lists, commitment tracking, and General Partner (GP) / Limited Partner (LP) splits.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 6

---

## 🎯 Sub-Deliverables

### 166.1 Kafka Syndication Deal Ingestion `[ ]`

**Acceptance Criteria**: Ingest syndicated deal opportunities from email parsers or APIs. Structure unstructured email data ("18% IRR projected!") into normalized DB records.

#### Kafka Topic

```json
{
    "topic": "deal-ingestion",
    "schema": {
        "source": "EMAIL_PARSER",
        "sender": "sponsor@syndicate.com",
        "deal_title": "string",
        "asset_class": "MULTIFAMILY",
        "projected_irr": "decimal",
        "equity_multiple": "decimal",
        "hold_period_years": "integer",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Email Parser | `services/ingestion/email_parser.py` | `[ ]` |
| Deal Consumer | `services/kafka/deal_consumer.py` | `[ ]` |

---

### 166.2 Postgres Operating Agreement Schema (GP/LP splits) `[ ]`

**Acceptance Criteria**: Track the complex "Waterfall" economics. Preferred Return (e.g., 8%), then Split (e.g., 70/30 LP/GP).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE syndication_economics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID NOT NULL,
    
    -- Waterfall
    preferred_return_pct DECIMAL(5, 4), -- 0.08
    gp_catchup_pct DECIMAL(5, 4),
    
    -- Splits
    tier1_split_lp DECIMAL(5, 4),       -- 0.70
    tier1_split_gp DECIMAL(5, 4),       -- 0.30
    promote_structure JSONB,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/166_syndication_econ.sql` | `[ ]` |
| Waterfall Calc | `services/pe/waterfall_calc.py` | `[ ]` |

---

### 166.3 Neo4j General Partner ↔ Limited Partner Nodes `[ ]`

**Acceptance Criteria**: Map relationships. An investor acts as LP in many deals, and a Sponsor acts as GP. Track "Repeat Sponsor" success rates.

```cypher
(:PERSON:GP {name: "Sponsor Inc"})-[:SPONSORED]->(:DEAL:SYNDICATION)
(:PERSON:LP {name: "Client"})-[:INVESTED_IN {amount: 50000}]->(:DEAL:SYNDICATION)

// Find repeat investments
MATCH (lp:LP)-[:INVESTED_IN]->(:DEAL)<-[:SPONSORED]-(gp:GP)
RETURN lp, gp, count(*) as deals_together
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Syndication Graph | `services/neo4j/syndication_graph.py` | `[ ]` |

---

### 166.4 Capital Raise Tracker (Apartments, Offices, Credit) `[ ]`

**Acceptance Criteria**: Track the progress of a raise. "Soft Circles" (Commitments) vs. "Funded" (Wire Received). prevent over-subscription.

| Component | File Path | Status |
|-----------|-----------|--------|
| Raise Tracker | `services/pe/raise_tracker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Deal Room | `frontend2/src/components/Syndication/DealRoom.jsx` | `[ ]` |
| Commitment Flow | `frontend2/src/components/Syndication/CommitmentFlow.jsx` | `[ ]` |

---

### 166.5 No Formal Offering Private Syndication Flag `[ ]`

**Acceptance Criteria**: Flag "506(b)" deals which CANNOT be advertised publicly and require a "Pre-existing substantive relationship". Ensure compliance by hiding these from public view.

| Component | File Path | Status |
|-----------|-----------|--------|
| Compliance Filter | `services/compliance/506b_filter.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py syndication list` | List open deals | `[ ]` |
| `python cli.py syndication commit <id>` | Soft commit to deal | `[ ]` |

---

*Last verified: 2026-01-25*
