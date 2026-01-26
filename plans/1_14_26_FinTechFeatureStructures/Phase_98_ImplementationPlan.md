# Phase 98: 'Unusual Whales' Copy-Trade Strategy

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Systematically follow "Flow". If deep ITM calls are bought on a random stock, follow it. Replicates "Unusual Whales" style logic but automated.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 98

---

## 🎯 Sub-Deliverables

### 98.1 Flow Feed Ingest `[ ]`

**Acceptance Criteria**: Ingest option flow. Filter for "Bullish Sentiment" (Ask side aggresion).

| Component | File Path | Status |
|-----------|-----------|--------|
| Flow Ingest | `services/ingestion/unusual_options.py` | `[ ]` |

---

### 98.2 'Golden Sweep' Detector `[ ]`

**Acceptance Criteria**: Multi-exchange sweep, large size, short expiry. Urgent buying.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweep Algo | `services/analysis/golden_sweep.py` | `[ ]` |

---

### 98.3 Copy-Trade Execution Logic `[ ]`

**Acceptance Criteria**: Logic to buy the same option (or underlying stock) with strict stop loss.

| Component | File Path | Status |
|-----------|-----------|--------|
| Executor | `services/strategies/flow_copy.py` | `[ ]` |

---

### 98.4 Win-Rate Backtester `[ ]`

**Acceptance Criteria**: Backtest this flow logic. "Do these whales actually know something?" (Filtering is key).

| Component | File Path | Status |
|-----------|-----------|--------|
| Backtester | `services/backtest/whale_strat.py` | `[ ]` |

### 98.5 Flow Heatmap `[ ]`

**Acceptance Criteria**: Visual heatmap. "Tech is seeing huge call buys today."

| Component | File Path | Status |
|-----------|-----------|--------|
| Heatmap | `frontend2/src/components/Options/FlowHeat.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py flow scan` | Top whales | `[ ]` |
| `python cli.py flow auto-trade` | Enable bot | `[ ]` |

---

*Last verified: 2026-01-25*
