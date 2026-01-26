# Phase 15: Institutional Logic-Based TA Primitives

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: AI Team

---

## 📋 Overview

**Description**: Decommission retail indicators and implement institutional primitives (Supply/Demand, GEX, Market Structure).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 15.1 Retail Indicator Purge `[ ]`

**Acceptance Criteria**: Disable and purge all standard RSI, MACD, and Bollinger Band modules from the SearcherAgent library.

| Component | File Path | Status |
|-----------|-----------|--------|
| Indicator Purge Script | `scripts/purge_retail_indicators.py` | `[ ]` |
| Deprecated Module List | `config/deprecated_indicators.py` | `[ ]` |

#### Purged Indicators

| Indicator | Reason | Status |
|-----------|--------|--------|
| RSI | Retail noise | `[ ]` |
| MACD | Lagging indicator | `[ ]` |
| Bollinger Bands | Mean reversion trap | `[ ]` |
| Moving Average Crossover | Predictable to institutions | `[ ]` |

---

### 15.2 Supply/Demand Zone Detection `[ ]`

**Acceptance Criteria**: Implement 'Supply and Demand' zone detection based on institutional liquidity pools and order blocks.

| Component | File Path | Status |
|-----------|-----------|--------|
| Zone Detector | `services/analysis/supply_demand_zones.py` | `[ ]` |
| Order Block Finder | `services/analysis/order_blocks.py` | `[ ]` |

---

### 15.3 GEX Monitoring for Indices `[ ]`

**Acceptance Criteria**: Configure Gamma Exposure (GEX) monitoring for SPY/QQQ to detect institutional turning points.

| Component | File Path | Status |
|-----------|-----------|--------|
| GEX Calculator | `services/options/gex_calculator.py` | `[ ]` |
| Gamma Flip Detector | `services/options/gamma_flip.py` | `[ ]` |

---

### 15.4 Neo4j LIQUIDITY_ZONE Nodes `[ ]`

**Acceptance Criteria**: Ensure all detected zones are mapped to Neo4j as `LIQUIDITY_ZONE` nodes for relationship analysis.

```cypher
(:LIQUIDITY_ZONE {
    id: "uuid",
    symbol: "EUR/USD",
    type: "SUPPLY",  // SUPPLY, DEMAND
    price_high: 1.0900,
    price_low: 1.0880,
    strength: 0.85,
    created_at: datetime(),
    mitigated: false
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Zone Graph Service | `services/neo4j/zone_graph.py` | `[ ]` |

---

### 15.5 Logic-Based Justification Logs `[ ]`

**Acceptance Criteria**: Log logic-based justifications for every detected trade setup, stripping away 'Retail BS' noise.

| Component | File Path | Status |
|-----------|-----------|--------|
| Logic Logger | `services/analysis/logic_logger.py` | `[ ]` |
| Justification Builder | `services/analysis/justification_builder.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 15.1 Retail Purge | `[ ]` | `[ ]` |
| 15.2 Supply/Demand | `[ ]` | `[ ]` |
| 15.3 GEX Monitoring | `[ ]` | `[ ]` |
| 15.4 Neo4j Zones | `[ ]` | `[ ]` |
| 15.5 Logic Logs | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
