# Phase 34: Institutional Alpha: Smart Money Order Flow

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Implement the ingestion and analysis of "Smart Money" order flow to detect institutional intent. Level 2 data, Order Imbalances, and "Whale" detecting algorithms. This separates the system from retail tools.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 34

---

## 🎯 Sub-Deliverables

### 34.1 Level 2 Data Stream Ingestion `[ ]`

**Acceptance Criteria**: Establish a Kafka stream for Level 2 Order Book data for Major Pairs. Handle high-velocity updates (Bids/Asks depth).

#### Kafka Topic

```json
{
    "topic": "l2-orderbook",
    "schema": {
        "ticker": "EURUSD",
        "bids": [[1.0850, 500], [1.0849, 1200]],
        "asks": [[1.0851, 300], [1.0852, 800]],
        "timestamp": "long"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| L2 Producer | `services/ingestion/l2_producer.py` | `[ ]` |

---

### 34.2 Neo4j 'Order Imbalance' Nodes `[ ]`

**Acceptance Criteria**: Map 'Order Blocks' and 'Inefficiencies' in the price action as nodes in Neo4j (e.g., `IMBALANCE {type: "BUY_SIDE", strength: 80}`).

| Component | File Path | Status |
|-----------|-----------|--------|
| Graph Mapper | `services/neo4j/imbalance_mapper.py` | `[ ]` |

---

### 34.3 Imbalance-to-Breakout Correlation `[ ]`

**Acceptance Criteria**: Calculate the correlation between order flow imbalance and subsequent price breakout. Does a 3:1 Bid/Ask ratio predict a pump?

| Component | File Path | Status |
|-----------|-----------|--------|
| Correlation Engine | `services/analysis/flow_correlation.py` | `[ ]` |

---

### 34.4 'Whale' Movement Detector `[ ]`

**Acceptance Criteria**: Identify "Iceberg" orders or massive single prints. Log to `market-telemetry`.

```python
class WhaleDetector:
    def check_print(self, trade: Trade) -> bool:
        if trade.size > self.get_whale_threshold(trade.symbol):
            self.kafka.emit("WHALE_ALERT", trade)
            return True
        return False
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Whale Detector | `services/market/whale_detector.py` | `[ ]` |

---

### 34.5 SearcherAgent Priority Logic `[ ]`

**Acceptance Criteria**: Verify that SearcherAgent weights Smart Money signals higher than technical patterns.

| Component | File Path | Status |
|-----------|-----------|--------|
| Agent Logic | `services/agents/searcher/priority_logic.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py flow check-l2` | View Depth | `[ ]` |
| `python cli.py flow list-whales` | Recent large trades | `[ ]` |

---

*Last verified: 2026-01-25*
