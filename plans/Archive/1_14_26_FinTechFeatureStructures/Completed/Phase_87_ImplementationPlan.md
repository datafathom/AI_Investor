# Phase 87: Lifecycle Investing (Leverage Management)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: Implement "Lifecycle Investing" (Ayres/Nalebuff). Young investors should use leverage (2:1) to diversify across time. As you age, deleverage. This phase manages that structural leverage safely.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 87

---

## 🎯 Sub-Deliverables

### 87.1 Age-Based Leverage Target `[x]`

**Acceptance Criteria**: Formula: `Target Leverage = 2.0 if Age < 30`. Glide path down to 1.0 at retirement.

| Component | File Path | Status |
|-----------|-----------|--------|
| Glide Path | `services/strategies/lifecycle_glide.py` | `[x]` |

---

### 87.2 Margin Cost Optimizer `[x]`

**Acceptance Criteria**: Compare cost of leverage (Box Spreads vs Margin Loan vs Futures). "Box Spreads are cheaper than Broker Margin."

| Component | File Path | Status |
|-----------|-----------|--------|
| Cost Opt | `services/analysis/leverage_cost.py` | `[x]` |

---

### 87.3 Deep ITM Call (LEAPS) Strategy `[x]`

**Acceptance Criteria**: Use deep ITM LEAPS (80 delta) as a non-callable form of leverage. "Stock Replacement Strategy".

| Component | File Path | Status |
|-----------|-----------|--------|
| LEAPS Strat | `services/strategies/leaps_replacement.py` | `[x]` |

---

### 87.4 Volatility Targeting (De-leveraging) `[x]`

**Acceptance Criteria**: If Volatility spikes, de-leverage immediately (Kelly Criterion). Leverage is for calm markets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Vol Target | `services/risk/vol_target.py` | `[x]` |

### 87.5 Retirement Date Simulator `[x]`

**Acceptance Criteria**: Sim: "If you use 1.5x leverage, you retire 5 years earlier (90% conf) or 2 years later (10% conf)."

| Component | File Path | Status |
|-----------|-----------|--------|
| Ret Sim | `services/simulation/retirement_leverage.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py lifecyc check` | Current lev ratio | `[x]` |
| `python cli.py lifecyc suggest` | Optimize lev | `[x]` |

---

*Last verified: 2026-01-25*
