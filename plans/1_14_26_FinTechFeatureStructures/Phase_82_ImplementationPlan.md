# Phase 82: Portfolio Rebalancing Automation (Tax-Aware)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Portfolio Team

---

## 📋 Overview

**Description**: Automate rebalancing execution. But be smart. Don't just sell winners (triggering tax). Buy underweight assets with new cash first ("Cash Flow Rebalancing").

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 82

---

## 🎯 Sub-Deliverables

### 82.1 'Drift' Visualizer `[ ]`

**Acceptance Criteria**: Visualize deviation from Target Allocation. Red Bar = Overweight. Green Bar = Underweight.

| Component | File Path | Status |
|-----------|-----------|--------|
| Drift UI | `frontend2/src/components/Portfolio/Drift.jsx` | `[ ]` |

---

### 82.2 Cash Flow Rebalancing Logic `[ ]`

**Acceptance Criteria**: Algorithm: "We need 5% more bonds. We have $10k cash. Buy bonds." Avoid selling stocks if possible.

| Component | File Path | Status |
|-----------|-----------|--------|
| Logic Engine | `services/strategies/smart_rebalance.py` | `[ ]` |

---

### 82.3 Tax Impact Estimator (Pre-Trade) `[ ]`

**Acceptance Criteria**: Before rebalancing, estimate tax bill. "Selling AAPL to rebalance will cost $5k in tax. Is it worth it?"

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Est | `services/tax/rebalance_impact.py` | `[ ]` |

---

### 82.4 Bulk Order Execution Generator `[ ]`

**Acceptance Criteria**: Generate a "Basket Order" (List of buys/sells) to execute the rebalance in one go.

| Component | File Path | Status |
|-----------|-----------|--------|
| Order Gen | `services/trading/bulk_orders.py` | `[ ]` |

### 82.5 Rebalancing Audit Log `[ ]`

**Acceptance Criteria**: Log reason for rebalance. "Quarterly Reset" vs "Drift Trigger".

| Component | File Path | Status |
|-----------|-----------|--------|
| Log | `services/logging/rebalance_log.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py rebalance check` | Show drift | `[ ]` |
| `python cli.py rebalance generate` | Create orders | `[ ]` |

---

*Last verified: 2026-01-25*
