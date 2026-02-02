# Phase 187: Geopolitical Risk & 'Total War' Simulator

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Extreme tail risk simulation (War, Supply Chain collapse).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 7

---

## 🎯 Sub-Deliverables

| Migration | `migrations/187_country_dep.sql` | `[ ]` |
| Dependency Mapper | `services/risk/dependency_mapper.py` | `[ ]` |

---

### 187.3 Market Efficiency Geopolitical Fear Score `[ ]`

**Acceptance Criteria**: "Fear Gauge". Measure implied volatility (VIX, MOVE Index, Gold Put/Call Skew) to quantify market fear.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fear Gauge | `services/market/fear_gauge.py` | `[ ]` |

---

### 187.4 Neo4j Sovereign Policy → Foreign Investment Node `[ ]`

**Acceptance Criteria**: Graph modeling of sanctions/tariffs. If "US" sanctions "Chip Exports", map the downstream effect on "Nvidia" revenues.

```cypher
(:COUNTRY {name: "USA"})-[:IMPOSES_SANCTION {sector: "SEMICONDUCTORS"}]->(:COUNTRY {name: "China"})
(:COMPANY {ticker: "NVDA"})-[:REVENUE_EXPOSURE {pct: 0.20}]->(:COUNTRY {name: "China"})

// Impact Query
MATCH (c:COMPANY)-[r:REVENUE_EXPOSURE]->(target:COUNTRY)<-[:IMPOSES_SANCTION]-(source:COUNTRY)
RETURN c.ticker, r.pct as revenue_at_risk
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sanction Graph | `services/neo4j/sanction_graph.py` | `[ ]` |

---

### 187.5 Betting Against Risk Entry Point Model `[ ]`

**Acceptance Criteria**: Logic for "buying blood". If the market prices in a 90% chance of catastrophe but our model says 60%, identify the Entry Point.

| Component | File Path | Status |
|-----------|-----------|--------|
| Entry Point Algo | `services/trading/contrarian_entry.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| War Room | `frontend2/src/components/Risk/WarRoom.jsx` | `[ ]` |
| Supply Chain Map | `frontend2/src/components/Maps/SupplyChainRisk.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py geo simulate <scenario>` | Run war game | `[ ]` |
| `python cli.py geo check-sanctions` | Check exposure | `[ ]` |

---

*Last verified: 2026-01-25*
