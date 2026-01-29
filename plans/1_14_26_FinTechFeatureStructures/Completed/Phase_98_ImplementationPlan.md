# Phase 98: 'Unusual Whales' Copy-Trade Strategy

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Systematically follow "Flow". If deep ITM calls are bought on a random stock, follow it. Replicates "Unusual Whales" style logic but automated.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 98

---

## 🎯 Sub-Deliverables

### 98.1 Flow Feed Ingest `[x]`

**Acceptance Criteria**: Ingest option flow. Filter for "Bullish Sentiment" (Ask side aggresion).

| Component | File Path | Status |
|-----------|-----------|--------|
| Flow Ingest | `services/ingestion/unusual_options.py` | `[x]` |

---

### 98.2 'Golden Sweep' Detector `[x]`

**Acceptance Criteria**: Multi-exchange sweep, large size, short expiry. Urgent buying.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweep Algo | `services/analysis/golden_sweep.py` | `[x]` |

---

### 98.3 Copy-Trade Execution Logic `[x]`

**Acceptance Criteria**: Logic to buy the same option (or underlying stock) with strict stop loss.

| Component | File Path | Status |
|-----------|-----------|--------|
| Executor | `services/strategies/flow_copy.py` | `[x]` |

---

### 98.4 Win-Rate Backtester `[x]`

**Acceptance Criteria**: Backtest this flow logic. "Do these whales actually know something?" (Filtering is key).

| Component | File Path | Status |
|-----------|-----------|--------|
| Backtester | `services/backtest/whale_strat.py` | `[x]` |

### 98.5 Flow Heatmap `[x]`

**Acceptance Criteria**: Visual heatmap. "Tech is seeing huge call buys today."

| Component | File Path | Status |
|-----------|-----------|--------|
| Heatmap | `frontend2/src/components/Options/FlowHeat.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py flow scan` | Top whales | `[x]` |
| `python cli.py flow auto-trade` | Enable bot | `[x]` |

---

*Last verified: 2026-01-25*
