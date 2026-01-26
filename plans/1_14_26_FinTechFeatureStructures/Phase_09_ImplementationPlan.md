# Phase 9: Currency Correlation Neo4j Edge Mapping

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Graph Database Team

---

## 📋 Overview

**Description**: Map real-time currency correlations as graph edges to detect and visualize ecosystem-wide contagion risk.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 9.1 Dynamic Edge Weight Updates `[ ]`

**Acceptance Criteria**: Implement dynamic edge weight updates in Neo4j based on 24-hour rolling correlation coefficients.

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Calculator | `services/correlation_calculator.py` | `[ ]` |
| Edge Weight Updater | `services/neo4j/edge_weight_updater.py` | `[ ]` |
| Rolling Window Service | `services/rolling_window.py` | `[ ]` |

#### Cypher Update Logic

```cypher
// Update correlation edge weight
MATCH (a1:ASSET {symbol: $symbol1})-[r:CORRELATED_WITH]->(a2:ASSET {symbol: $symbol2})
SET r.coefficient = $coefficient,
    r.confidence = $confidence,
    r.updated_at = datetime()
RETURN r
```

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Correlation | `tests/unit/test_correlation_calculator.py` | `[ ]` |
| Integration: Edge Updates | `tests/integration/test_edge_updates.py` | `[ ]` |

---

### 9.2 CORRELATED_WITH Attributes `[ ]`

**Acceptance Criteria**: Define `CORRELATED_WITH` attributes: Coefficient, Confidence Level, and Timeframe (e.g., 1H, 4H, 1D).

#### Relationship Schema

```cypher
// CORRELATED_WITH relationship properties
(:ASSET)-[:CORRELATED_WITH {
    coefficient: 0.85,      // -1.0 to 1.0
    confidence: 0.92,       // 0.0 to 1.0
    timeframe: "1D",        // 1H, 4H, 1D, 1W
    sample_size: 288,       // Number of data points
    p_value: 0.001,         // Statistical significance
    direction: "POSITIVE",  // POSITIVE, NEGATIVE, NEUTRAL
    updated_at: datetime()
}]->(:ASSET)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Schema | `neo4j/schema/003_correlations.cypher` | `[ ]` |
| Attribute Validator | `services/neo4j/correlation_validator.py` | `[ ]` |

---

### 9.3 Contagion Cluster Queries `[ ]`

**Acceptance Criteria**: Develop Cypher queries to identify 'Contagion Clusters' where multiple assets are moving in unison.

#### Cypher Queries

```cypher
// Find contagion clusters (assets with correlation > 0.8)
MATCH (a1:ASSET)-[r:CORRELATED_WITH]->(a2:ASSET)
WHERE r.coefficient > 0.8 AND r.timeframe = '1D'
WITH a1, collect({asset: a2, correlation: r.coefficient}) AS correlations
WHERE size(correlations) >= 3
RETURN a1.symbol AS hub, correlations
ORDER BY size(correlations) DESC

// Detect systemic risk (all assets moving together)
MATCH path = (a1:ASSET)-[:CORRELATED_WITH*1..3]->(a2:ASSET)
WHERE ALL(r IN relationships(path) WHERE r.coefficient > 0.9)
RETURN path
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Contagion Detector | `services/neo4j/contagion_detector.py` | `[ ]` |
| Query Builder | `services/neo4j/correlation_queries.py` | `[ ]` |

---

### 9.4 Graph Price Responsiveness `[ ]`

**Acceptance Criteria**: Verify graph responsiveness to price updates driven by the Redpanda `market-telemetry` stream.

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Update Latency | < 500ms | - | `[ ]` |
| Correlation Recalc | < 2s | - | `[ ]` |
| Edge Count (6 pairs) | 15 edges | - | `[ ]` |

| Component | File Path | Status |
|-----------|-----------|--------|
| Kafka Graph Bridge | `services/kafka/graph_bridge.py` | `[ ]` |
| Price Event Handler | `services/neo4j/price_event_handler.py` | `[ ]` |

---

### 9.5 Correlation Matrix GUI `[ ]`

**Acceptance Criteria**: Display a color-coded correlation matrix within the GUI to highlight positive vs. negative correlation risks.

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Matrix | `frontend2/src/components/CorrelationMatrix/CorrelationMatrix.jsx` | `[ ]` |
| Matrix Cell | `frontend2/src/components/CorrelationMatrix/MatrixCell.jsx` | `[ ]` |
| Color Scale | `frontend2/src/utils/correlationColors.js` | `[ ]` |

#### Color Coding

| Correlation Range | Color | Meaning |
|-------------------|-------|---------|
| 0.8 to 1.0 | Deep Red | High positive (contagion risk) |
| 0.5 to 0.8 | Orange | Moderate positive |
| -0.5 to 0.5 | Gray | Low/no correlation |
| -0.8 to -0.5 | Light Blue | Moderate negative (hedge) |
| -1.0 to -0.8 | Deep Blue | Strong negative (safe hedge) |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 9.1 Edge Weight Updates | `[ ]` | `[ ]` |
| 9.2 CORRELATED_WITH Attrs | `[ ]` | `[ ]` |
| 9.3 Contagion Queries | `[ ]` | `[ ]` |
| 9.4 Price Responsiveness | `[ ]` | `[ ]` |
| 9.5 Correlation Matrix | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py correlation-matrix` | Display correlation matrix | `[ ]` |
| `python cli.py contagion-scan` | Scan for contagion clusters | `[ ]` |

---

## 📦 Dependencies

- Phase 2: FX Stream Topic (price data source)
- Phase 4: Neo4j Graph Schema (node structure)

---

*Last verified: 2026-01-25*
