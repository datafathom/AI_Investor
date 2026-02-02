# Phase 194: Bank Sweep Revenue & Overnight Liquidity Tracker

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Treasury Team

---

## 📋 Overview

**Description**: Manage cash. Brokerages make billions by sweeping client cash into low-yield accounts.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 14

---

## 🎯 Sub-Deliverables

### 194.1 Cash Drag Alert System `[x]`

**Acceptance Criteria**: Alert if uninvested cash > 2% of portfolio.

| Component | File Path | Status |
|-----------|-----------|--------|
| Drag Monitor | `services/alerts/cash_drag.py` | `[x]` |

---

### 194.2 Auto-Sweep to Treasury Money Market `[x]`

**Acceptance Criteria**: Execution logic. Buy cash-equivalent ETFs (SGOV, BIL).

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweep Engine | `services/trading/bank_sweep_executor.py` | `[x]` |

---

### 194.3 Postgres Interest Rate Arb Log `[x]`

**Acceptance Criteria**: Track "Lost Opportunity Cost".

| Component | File Path | Status |
|-----------|-----------|--------|
| Arb Calculator | `services/banking/sweep_tracker.py` | `[x]` |

---

### 194.4 FDIC Insurance Limit Breaker (>$250k) `[x]`

**Acceptance Criteria**: Split cash across multiple banks.

| Component | File Path | Status |
|-----------|-----------|--------|
| FDIC Optimizer | `services/treasury/fdic_split.py` | `[x]` |

---

### 194.5 Treasury Ladder Builder (4-Week, 8-Week Bills) `[x]`

**Acceptance Criteria**: Build a "T-Bill Ladder".

| Component | File Path | Status |
|-----------|-----------|--------|
| Ladder Builder | `services/strategies/ladder_builder.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py treasury sweep` | Run auto sweep | `[x]` |
| `python cli.py treasury show-lost` | Show lost interest | `[x]` |

---

*Last verified: 2026-01-30*


---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py treasury sweep` | Run auto sweep | `[ ]` |
| `python cli.py treasury show-lost` | Show lost interest | `[ ]` |

---

*Last verified: 2026-01-25*
