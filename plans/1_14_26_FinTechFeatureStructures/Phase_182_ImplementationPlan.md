# Phase 182: Michael Green 'Big Three' Reflexivity Index

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Passive investment bubble risk (Inelastic Market Hypothesis).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 2

---

## 🎯 Sub-Deliverables

### 182.1 Reflexivity Index (BlackRock, Vanguard, State Street) `[x]`

**Acceptance Criteria**: Calculate Passive Ownership %.

```python
class ReflexivityCalculator:
    """
    Calculate Passive Ownership Score.
    
    Data Source: 13F Filings.
    Sum(Holdings of 'Big Three') / TotalSharesOutstanding.
    """
    def calculate_score(self, ticker: str) -> float:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Calculator | `services/quantitative/reflexivity_engine.py` | `[x]` |
| 13F Analyzer | `services/ingestion/13f_analyzer.py` | `[ ]` |

---

### 182.2 Postgres 40% Market Share Threshold Flag `[x]`

**Acceptance Criteria**: DB flag for high-passive stocks.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE passive_saturation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    
    -- Ownership
    vanguard_pct DECIMAL(5, 4),
    blackrock_pct DECIMAL(5, 4),
    statestreet_pct DECIMAL(5, 4),
    total_passive_pct DECIMAL(5, 4),
    
    -- Risk
    is_saturated BOOLEAN GENERATED ALWAYS AS (total_passive_pct > 0.40) STORED,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/182_passive_saturation.sql` | `[ ]` |
| Saturation Monitor | `services/risk/saturation_monitor.py` | `[ ]` |

---

### 182.3 Neo4j Blind 401k Inflows → Index Distortion Node `[ ]`

**Acceptance Criteria**: Graph model showing how 401k bi-weekly contributions (blind flows) mechanically pump the largest stocks.

```cypher
(:FLOW:401K_CONTRIB)-[:FORCED_BUY]->(:INDEX:SP500)
(:INDEX:SP500)-[:MECHANICAL_BID]->(:STOCK:AAPL)
(:INDEX:SP500)-[:MECHANICAL_BID]->(:STOCK:MSFT)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Flow Graph | `services/neo4j/flow_graph.py` | `[ ]` |

---

### 182.4 Sorosian Reflexivity Price → Flow Simulator `[ ]`

**Acceptance Criteria**: Simulator based on George Soros's concept. Higher Prices → More Index Inflows → Higher Prices (Feedback Loop). And the reverse crash.

| Component | File Path | Status |
|-----------|-----------|--------|
| Feedback Loop Sim | `services/simulation/reflexivity_sim.py` | `[ ]` |

---

### 182.5 Ticking Time Bomb 401k Net Outflow Alert `[ ]`

**Acceptance Criteria**: Alert when Boomer Retirements (withdrawals) > Gen Z Contributions. Net selling pressure could pop the passive bubble.

| Component | File Path | Status |
|-----------|-----------|--------|
| Demographic Alert | `services/alerts/demographic_risk.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Passive Risk Map | `frontend2/src/components/Risk/PassiveMap.jsx` | `[ ]` |
| Flow Monitor | `frontend2/src/components/Charts/FlowMonitor.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py reflex check-stock <ticker>` | Show passive % | `[ ]` |
| `python cli.py reflex sim-crash` | Sim passive unwind | `[ ]` |

---

*Last verified: 2026-01-25*
