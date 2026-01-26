# Phase 65: Section 16 Insider Trading Monitor (Form 4)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Alternative Data Team

---

## 📋 Overview

**Description**: Track Corporate Insiders (CEOs, CFOs) buying their own stock. "Insiders sell for many reasons, but they buy for only one: they think the price will go up." (Peter Lynch).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 65

---

## 🎯 Sub-Deliverables

### 65.1 SEC Form 4 Real-Time Feed `[ ]`

**Acceptance Criteria**: Poll SEC EDGAR every 60 seconds for Form 4 filings. Filter for "P - Open Market Purchase". Ignore "Option Exercises".

| Component | File Path | Status |
|-----------|-----------|--------|
| Edgar Poller | `services/ingestion/form4_poller.py` | `[ ]` |

---

### 65.2 'Cluster Buy' Detection `[ ]`

**Acceptance Criteria**: Detect when multiple insiders (CEO + CFO + Director) buy within a 7-day window. "Cluster Buying" is the strongest signal.

```python
class ClusterDetector:
    def check(self, ticker):
        recent_buys = self.db.get_buys(ticker, days=7)
        if len(set(b.insider_name for b in recent_buys)) >= 3:
            self.alerts.trigger("CLUSTER_BUY", ticker)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Cluster Engine | `services/analysis/insider_cluster.py` | `[ ]` |

---

### 65.3 Historical Win Rate Backtest `[ ]`

**Acceptance Criteria**: Backtest: If we bought every time the CEO bought >$100k, what is the 6-month return?

| Component | File Path | Status |
|-----------|-----------|--------|
| Backtester | `services/backtest/insider_strat.py` | `[ ]` |

---

### 65.4 Neo4j Insider Graph `[ ]`

**Acceptance Criteria**: Map relationships. `(:PERSON)-[:IS_CEO_OF]->(:COMPANY)`. Track "Super Insiders" who have a history of timed buys.

| Component | File Path | Status |
|-----------|-----------|--------|
| Insider Graph | `services/neo4j/insider_graph.py` | `[ ]` |

### 65.5 Significant Purchase Alert (>$500k) `[ ]`

**Acceptance Criteria**: Filter out token small buys. Alert only on "High Conviction" purchases > $500k.

| Component | File Path | Status |
|-----------|-----------|--------|
| Alert Filter | `services/alerts/high_conviction.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py insider monitor` | Start polling | `[ ]` |
| `python cli.py insider stats <ticker>` | Show CEO track record | `[ ]` |

---

*Last verified: 2026-01-25*
