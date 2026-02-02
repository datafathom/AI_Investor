# Phase 174: Alternative Asset Diversification Multi-Node

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Portfolio Team

---

## 📋 Overview

**Description**: Broaden the definition of "Alternatives". Integrate non-traditional assets like Fine Art, Collectibles (Cars, Watches), Litigation Finance, and Crypto. Map their correlations (often 0) to standard markets.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 14

---

## 🎯 Sub-Deliverables

### 174.1 Neo4j Specialized Asset Nodes (Art, Wine, Crypto) `[ ]`

**Acceptance Criteria**: Create distinct asset classes in the graph. Art behaves differently than Gold.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:ASSET_CLASS:ART {
    name: "Blue Chip Art",
    correlation_sp500: 0.1,
    liquidity: "VERY_LOW"
})

(:ASSET_CLASS:LITIGATION_FINANCE {
    name: "Legal Claims",
    correlation_sp500: -0.05,
    yield: 0.12
})

(:ASSET_CLASS:CRYPTO {
    name: "Bitcoin",
    volatility: 0.80
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Alts Graph Service | `services/neo4j/alts_graph.py` | `[ ]` |

---

### 174.2 Valuation Feed Adapter (Masterworks, Chrono24) `[ ]`

**Acceptance Criteria**: Adapters to fetch pricing for these esoteric assets. Masterworks for Art, Chrono24/StockX for collectibles.

| Component | File Path | Status |
|-----------|-----------|--------|
| Art Valuator | `services/external/masterworks_adapter.py` | `[ ]` |
| Watch Valuator | `services/external/chrono24_adapter.py` | `[ ]` |

---

### 174.3 Storage & Insurance Cost Tracker `[ ]`

**Acceptance Criteria**: Track the "Negative Carry" (costs) of holding physical assets. Storage, Insurance, Appraisal fees.

#### Postgres Schema

```sql
CREATE TABLE physical_asset_costs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    cost_type VARCHAR(50),             -- INSURANCE, STORAGE, APPRAISAL
    annual_amount DECIMAL(20, 2),
    renewal_date DATE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/174_physical_costs.sql` | `[ ]` |
| Cost Tracker | `services/alts/cost_tracker.py` | `[ ]` |

---

### 174.4 "Passion Asset" Emotional Value Weighting `[ ]`

**Acceptance Criteria**: Allow users to overweight assets they "Love" (e.g., Classic Cars) using an "Emotional Utility" factor in the optimization model, essentially ignoring some financial inefficiency.

| Component | File Path | Status |
|-----------|-----------|--------|
| Utility Optimizer | `services/portfolio/emotional_utility.py` | `[ ]` |

---

### 174.5 K-1 Tax Document Aggregator `[ ]`

**Acceptance Criteria**: System to track and chase Schedule K-1 tax forms, which are notorious for arriving late (Aug/Sept) for alternative investments.

| Component | File Path | Status |
|-----------|-----------|--------|
| K1 Tracker | `services/tax/k1_tracker.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Alts Dashboard | `frontend2/src/components/Alts/Dashboard.jsx` | `[ ]` |
| K1 Status | `frontend2/src/components/Tax/K1Status.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py alts update-prices` | Fetch external valuations | `[ ]` |
| `python cli.py alts list-k1s` | Show missing K-1s | `[ ]` |

---

*Last verified: 2026-01-25*
