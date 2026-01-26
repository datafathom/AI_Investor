# Phase 41: Commodities & Alternative Alpha Ingestion

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Ingest price data for Gold, Oil, and other commodities. These serve as non-correlated hedges against currency devaluation and equity volatility.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 41

---

## 🎯 Sub-Deliverables

### 41.1 Kafka Commodity Feed (Gold/Oil) `[ ]`

**Acceptance Criteria**: Configure Kafka topics (`commodity-stream-global`) for real-time futures pricing (XAU/USD, CL=F) from providers.

| Component | File Path | Status |
|-----------|-----------|--------|
| Feed Config | `config/kafka/commodities.json` | `[ ]` |
| Ingestor | `services/ingestion/commodity_stream.py` | `[ ]` |

---

### 41.2 Contango/Backwardation Detector `[ ]`

**Acceptance Criteria**: Implement detection for the oil energy market term structure. Backwardation (Spot > Future) often signals physical shortage (Bullish).

```python
class TermStructureAnalyzer:
    def analyze_curve(self, spot: float, future_price: float) -> MarketState:
        if spot > future_price:
            return MarketState.BACKWARDATION
        return MarketState.CONTANGO
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Curve Analyzer | `services/analysis/term_structure.py` | `[ ]` |

---

### 41.3 Neo4j Gold-USD Inverse Correlation `[ ]`

**Acceptance Criteria**: Verify and map the negative correlation between Gold prices and USD index (DXY) strength in Neo4j.

| Component | File Path | Status |
|-----------|-----------|--------|
| Correction Graph | `services/neo4j/gold_usd.py` | `[ ]` |

---

### 41.4 Commodity-Weighted Inflation Baseline `[ ]`

**Acceptance Criteria**: Develop a commodity-weighted index tracker (like CRB Index) to serve as a real-time inflation-shielding baseline.

| Component | File Path | Status |
|-----------|-----------|--------|
| Inflation Index | `services/analysis/inflation_index.py` | `[ ]` |

### 41.5 Hedge Trade Logger `[ ]`

**Acceptance Criteria**: Log all commodity-driven hedge trades to the ProtectorAgent’s capital shielding journal.

| Component | File Path | Status |
|-----------|-----------|--------|
| Hedge Log | `services/logging/hedge_journal.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py comm check-curve` | Contango/Back | `[ ]` |
| `python cli.py comm get-gold` | XAU/USD price | `[ ]` |

---

*Last verified: 2026-01-25*
