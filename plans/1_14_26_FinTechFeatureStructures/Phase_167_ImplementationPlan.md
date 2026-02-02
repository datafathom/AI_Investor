# Phase 167: Borrowing Against Concentrated Stock (UHNW)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Private Banking & Lending Team

---

## 📋 Overview

**Description**: UHNW stock-based lending with PVFC and margin loans.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 7

---

## 🎯 Sub-Deliverables

### 167.1 Stock Loan Service `[x]`

**Acceptance Criteria**: LTV calculation based on volatility.

| Component | File Path | Status |
|-----------|-----------|--------|
| Lending Engine | `services/lending/stock_lending_svc.py` | `[x]` |

---

### 167.2 Interest-Tax Spread Analyzer `[x]`

**Acceptance Criteria**: Borrow cost vs sell tax analysis.

| Component | File Path | Status |
|-----------|-----------|--------|
| Spread Analyzer | `services/analysis/borrow_vs_sell.py` | `[x]` |

---

### 167.3 Kafka Margin Call Alert `[x]`

**Acceptance Criteria**: Collateral drop monitoring and alerts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Alert Producer | `services/kafka/collateral_monitor.py` | `[x]` |

---

### 167.4 Neo4j Concentrated Position ↔ Lending Bank `[x]`

**Acceptance Criteria**: Pledge relationship and control agreement mapping.

| Component | File Path | Status |
|-----------|-----------|--------|
| Collateral Graph | `services/neo4j/lending_graph.py` | `[x]` |

---

### 167.5 Interest-Only Payment Schedule Tracker `[x]`

**Acceptance Criteria**: Track IO credit lines until liquidity event.

| Component | File Path | Status |
|-----------|-----------|--------|
| Payment Tracker | `services/lending/payment_sched.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py lend calc-capacity` | Check borrow limit | `[x]` |
| `python cli.py lend analyze-spread` | Borrow vs Sell | `[x]` |

---

*Last verified: 2026-01-30*

