# Phase 24: Logic-Based Liquidity Zone Mapping (Neo4j)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Map institutional supply and demand zones within Neo4j to visualize and avoid "Smart Money" traps. Unlike retail "Support/Resistance" lines, these are dynamic zones defined by volume profile and order blocks.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 24

---

## 🎯 Sub-Deliverables

### 24.1 Neo4j `LIQUIDITY_ZONE` Node Schema `[x]`

**Acceptance Criteria**: Implement nodes with attributes: Type (Supply/Demand), Volume Profile, Strength (Touched count), and Timeframe (4H, Daily).

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
(:ASSET {ticker: "EURUSD"})-[:HAS_ZONE]->(:LIQUIDITY_ZONE {
    type: "SUPPLY",
    price_low: 1.0850,
    price_high: 1.0865,
    volume_at_zone: 50000,
    created_at: timestamp(),
    is_mitigated: false
})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Graph Service | `services/neo4j/liquidity_graph.py` | `[x]` |

---

### 24.2 Order Block Detection Algorithm `[x]`

**Acceptance Criteria**: Algorithm to identify "Order Blocks" (last down candle before strong up move, or vice versa) and push them to Neo4j.

```python
class OrderBlockDetector:
    def detect(self, candles: list[Candle]) -> list[Zone]:
        # Logic: Find impulsive move > 3x ATR
        # Flag preceding consolidation candle as OB
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| OB Detector | `services/analysis/order_blocks.py` | `[x]` |

---

### 24.3 Zone Mitigation Tracker `[x]`

**Acceptance Criteria**: Configure graph traversals to detect when a zone has been "violated" or "mitigated" (price tapped it and rejected, or blasted through). Mark node as `is_mitigated = true`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Mitigation Service | `services/analysis/zone_mitigation.py` | `[x]` |

---

### 24.4 Nearest 3-Trap Query (<100ms) `[x]`

**Acceptance Criteria**: Optimize Cypher query to find the nearest overhead Supply and nearest support Demand relative to current price.

```cypher
MATCH (a:ASSET {ticker: "EURUSD"})-[:HAS_ZONE]->(z:LIQUIDITY_ZONE)
WHERE z.is_mitigated = false AND z.price_low > 1.0800
RETURN z ORDER BY z.price_low ASC LIMIT 3
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Query Optimizer | `services/neo4j/queries/zone_queries.cql` | `[x]` |

---

### 24.5 SearcherAgent Zone Filter `[x]`

**Acceptance Criteria**: Integrate graph zones into SearcherAgent. DO NOT BUY if price is inside a Supply Zone.

| Component | File Path | Status |
|-----------|-----------|--------|
| Signal Filter | `services/strategies/zone_filter.py` | `[x]` |

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py zones detect <ticker>` | Find new zones | `[x]` |
| `python cli.py zones list-active` | Show unmitigated | `[x]` |

---

*Last verified: 2026-01-25*
