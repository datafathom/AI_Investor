# Phase 172: Illiquid Asset Premium & Volatility Smoother

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Quantitative & Risk Team

---

## 📋 Overview

**Description**: Illiquidity premium calculation and volatility unsmoothing.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 12

---

## 🎯 Sub-Deliverables

### 172.1 Illiquidity Premium Calculator `[x]`

**Acceptance Criteria**: Verify 3-5% premium over public markets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Premium Calculator | `services/private_markets/premium_optimizer.py` | `[x]` |

---

### 172.2 Return "Unsmoothing" Algorithm `[x]`

**Acceptance Criteria**: True volatility estimation via Geltner Index.

| Component | File Path | Status |
|-----------|-----------|--------|
| Unsmoother Service | `services/risk/volatility_unsmoother.py` | `[x]` |

---

### 172.3 Lock-Up Period Tracker `[x]`

**Acceptance Criteria**: Liquidity schedules and redemption windows.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liquidity Model | `services/real_estate/liquidity_model.py` | `[x]` |
| Illiquid Tracker | `services/wealth/illiquid_tracker.py` | `[x]` |

---

### 172.4 True Sharpe Ratio (Unsmoothed) Service `[x]`

**Acceptance Criteria**: Calculate Sharpe using true volatility.

| Component | File Path | Status |
|-----------|-----------|--------|
| True Sharpe Calc | `services/performance/true_sharpe.py` | `[x]` |

---

### 172.5 Secondary Market Valuation Discount Estimator `[x]`

**Acceptance Criteria**: NAV haircut estimation.

| Component | File Path | Status |
|-----------|-----------|--------|
| Discount Estimator | `services/valuation/secondary_market.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py priv calc-premium` | Show premium | `[x]` |
| `python cli.py priv unsmooth <id>` | Show true volatility | `[x]` |

---

*Last verified: 2026-01-30*

