# Phase 133: Standard Deviation & Volatility Refinement

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Refine volatility metrics to support advanced risk management. Moving beyond simple standard deviation to rolling metrics, daily price return ingestion via Kafka, and outlier filtering to distinguish "good" volatility (upside) from "bad" volatility (crashes).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 13

---

## 🎯 Sub-Deliverables

### 133.1 Rolling 1-Year/3-Year Std Dev Function `[x]`

**Acceptance Criteria**: Implement rolling window calculations for standard deviation to visualize how risk changes over time (e.g., during 2020 crash vs. 2021 bull run).

| Component | File Path | Status |
|-----------|-----------|--------|
| Rolling Volatility | `services/quantitative/rolling_volatility.py` | `[x]` |
| Window Manager | `services/data/window_manager.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Rolling Vol Chart | `frontend2/src/components/Charts/RollingVolatility.jsx` | `[x]` |

### 133.2 Daily Price Return Kafka Producer `[x]`

**Acceptance Criteria**: Configure a Kafka producer to stream daily price returns for all tracked assets to power real-time risk metrics.

#### Kafka Topic

```json
{
    "topic": "asset-returns-daily",
    "partitions": 4,
    "schema": {
        "ticker": "string",
        "date": "date",
        "close_price": "decimal",
        "daily_return": "decimal",
        "log_return": "decimal",
        "volume": "integer",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Returns Producer | `services/kafka/returns_producer.py` | `[x]` |
| Price Ingester | `services/market/price_ingester.py` | `[x]` |

### 133.3 High Volatility Outlier Filter `[x]`

**Acceptance Criteria**: Filter extreme outlier events (3+ sigma moves) to analyze tail risk separately from normal volatility.

| Component | File Path | Status |
|-----------|-----------|--------|
| Outlier Detector | `services/quantitative/outlier_detector.py` | `[x]` |
| Tail Risk Analyzer | `services/risk/tail_risk_analyzer.py` | `[x]` |

### 133.4 Neo4j Volatility Event → Asset Relationships `[x]`

**Acceptance Criteria**: Map specific volatility events (earnings, macro news) to assets in Neo4j to understand risk drivers.

```cypher
(:VOLATILITY_EVENT {
    id: "uuid",
    type: "EARNINGS_MISS",
    magnitude_sigma: 4.5,
    date: date()
})

(:ASSET)-[:EXPERIENCED_EVENT {
    price_drop: -0.15
}]->(:VOLATILITY_EVENT)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Event Mapper | `services/neo4j/volatility_event_mapper.py` | `[x]` |

### 133.5 SMA Securities Std Dev Verification `[x]`

**Acceptance Criteria**: Verify that Separately Managed Accounts (SMAs) are actually delivering the lower volatility they promise compared to the benchmark.

| Component | File Path | Status |
|-----------|-----------|--------|
| SMA Verifier | `services/compliance/sma_risk_verifier.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py vol rolling <ticker>` | Show rolling volatility | `[x]` |
| `python cli.py vol outliers <ticker>` | List outlier events | `[x]` |

---

*Last verified: 2026-01-25*
