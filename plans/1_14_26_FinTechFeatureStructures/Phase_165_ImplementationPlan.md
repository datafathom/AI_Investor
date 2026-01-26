# Phase 165: Venture Capital 'Cream of the Crop' Deal Flow

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Venture Capital Team

---

## 📋 Overview

**Description**: Manage Venture Capital investments, focusing on the "Power Law" nature of VC (1 home run pays for 99 failures). Implement systems to access and track top-tier deal flow, realizing that in VC, "Access is Alpha".

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 5

---

## 🎯 Sub-Deliverables

### 165.1 Accredited Investor Deal Flow List Service `[ ]`

**Acceptance Criteria**: Service to aggregate and curate deal flow from various sources (AngelList, Syndicates, Direct). Filter for quality signal (e.g., "Led by Sequoia").

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE vc_deal_flow (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_name VARCHAR(100),
    sector VARCHAR(50),                -- AI, SAAS, BIOTECH
    stage VARCHAR(20),                 -- SEED, SERIES_A, LATE
    
    -- Signal
    lead_investor VARCHAR(100),
    valuation_cap DECIMAL(20, 2),
    min_check_size DECIMAL(20, 2),
    
    -- Status
    status VARCHAR(20),                -- REVIEWING, PASSED, COMMITTED
    closing_date DATE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/165_vc_deals.sql` | `[ ]` |
| Deal Aggregator | `services/vc/deal_aggregator.py` | `[ ]` |

---

### 165.2 Postgres Top 8 VC Firm Access Table (Sequoia, a16z) `[ ]`

**Acceptance Criteria**: Database of "Tier 1" firms. Deals led by these firms get a "Gold Star" flag in the UI, as historical data shows they capture the vast majority of VC returns.

| Component | File Path | Status |
|-----------|-----------|--------|
| Tier1 Scorer | `services/vc/tier1_scorer.py` | `[ ]` |
| Config | `config/tier1_vc_firms.json` | `[ ]` |

---

### 165.3 Neo4j Entrepreneur ↔ VC Backer Graph `[ ]`

**Acceptance Criteria**: Graph network showing which VCs backed which Founders. Useful for identifying "Serial Entrepreneurs" who have previously made money for investors.

#### Neo4j Schema

```cypher
(:PERSON:FOUNDER {name: "Elon Musk"})-[:FOUNDED]->(:COMPANY {name: "SpaceX"})
(:VC_FIRM {name: "Founders Fund"})-[:INVESTED_IN]->(:COMPANY {name: "SpaceX"})

// Query: Find VCs who backed successful founders early
MATCH (f:FOUNDER)-[:FOUNDED]->(c:COMPANY)<-[:INVESTED_IN]-(vc:VC_FIRM)
WHERE c.exit_value > 1000000000
RETURN vc.name, count(c) as unicorns
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Network Graph | `services/neo4j/vc_network.py` | `[ ]` |

---

### 165.4 Unconventional 'Diamond in the Rough' Engine `[ ]`

**Acceptance Criteria**: Logic to flag deals that *don't* fit the standard pattern but have high potential (Contrarian bets). E.g., unusual background founders, neglected sectors.

| Component | File Path | Status |
|-----------|-----------|--------|
| Contrarian Detector | `services/vc/contrarian_detector.py` | `[ ]` |

---

### 165.5 Power-Law VC Alpha Model (1 deal = 90% returns) `[ ]`

**Acceptance Criteria**: Portfolio construction model effectively forcing diversification (min 20-50 startups) to ensure a statistical chance of hitting a Power Law "Fund Returner".

```python
class PowerLawSimulator:
    """
    Simulate VC Portfolio outcomes.
    
    Assumptions:
    - 50% go to zero.
    - 30% return 1x-3x.
    - 15% return 3x-10x.
    - 5% return 100x (The "Fund Returners").
    """
    
    def simulate_portfolio(self, num_investments: int) -> SimulationStats:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Simulator | `services/simulation/power_law.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Deal Flow Board | `frontend2/src/components/VC/DealFlowBoard.jsx` | `[ ]` |
| Portfolio Sim | `frontend2/src/components/Simulator/PowerLawSim.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py vc list-deals` | Show active deals | `[ ]` |
| `python cli.py vc simulate <count>` | Run power law sim | `[ ]` |

---

*Last verified: 2026-01-25*
