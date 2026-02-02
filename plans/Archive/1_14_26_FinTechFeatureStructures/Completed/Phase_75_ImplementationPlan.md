# Phase 75: Hedge Fund Replication (13F + TF)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Combine 13F Clone (Fundamental) with Trend Following (Technical) to replicate Hedge Fund performance without the 2/20 fees.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 75

---

## 🎯 Sub-Deliverables

### 75.1 Factor Replication Model `[x]`

**Acceptance Criteria**: Replicate returns using factors (Momentum, Value, Quality). If a Hedge Fund is just "Leveraged Beta", we can replicate it with ETFs.

| Component | File Path | Status |
|-----------|-----------|--------|
| Factor Model | `services/analysis/factor_rep.py` | `[x]` |

---

### 75.2 'Guru' ETF Basket Creator `[x]`

**Acceptance Criteria**: Create custom ETF baskets. "The Billionaire Basket". Top 20 stocks held by the top 20 managers.

| Component | File Path | Status |
|-----------|-----------|--------|
| Basket Gen | `services/strategies/basket_gen.py` | `[x]` |

---

### 75.3 Fee Drag Comparison Tool `[x]`

**Acceptance Criteria**: Visualizer. "Hedge Fund vs Replication". Show the compounding effect of saving 2% fees over 20 years.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Compare | `frontend2/src/components/Analysis/FeeDrag.jsx` | `[x]` |

---

### 75.4 Correlation Alert `[x]`

**Acceptance Criteria**: If replication correlation drops < 80%, the clone is failing. Alert user.

| Component | File Path | Status |
|-----------|-----------|--------|
| Corr Monitor | `services/alerts/clone_fail.py` | `[x]` |

### 75.5 Automated Rebalancing (Quarterly) `[x]`

**Acceptance Criteria**: Auto-rebalance the clone portfolio 45 days after quarter end (when 13Fs drop).

| Component | File Path | Status |
|-----------|-----------|--------|
| Rebalancer | `services/strategies/clone_rebalance.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py clone build <manager>` | Create portfolio | `[x]` |
| `python cli.py clone backtest` | Verify performance | `[x]` |

---

*Last verified: 2026-01-25*
