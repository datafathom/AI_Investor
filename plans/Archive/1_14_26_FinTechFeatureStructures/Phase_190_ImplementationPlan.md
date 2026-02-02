# Phase 190: Michael Green 'Forced Seller' Liquidity Tracker

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Model the "Forced Seller" dynamic in markets.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 10

---

## 🎯 Sub-Deliverables

### 190.1 Risk Parity De-leveraging Signal `[x]`

**Acceptance Criteria**: Monitor volatility relative to historical norms.

| Component | File Path | Status |
|-----------|-----------|--------|
| Volatility Monitor | `services/risk/vol_monitor.py` | `[x]` |
| Selling Predictor | `services/strategies/risk_parity.py` | `[x]` |

---

### 190.2 Margin Debt Contraction Monitor `[x]`

**Acceptance Criteria**: Track FINRA Margin Debt levels.

| Component | File Path | Status |
|-----------|-----------|--------|
| Margin Tracker | `services/market/finra_margin.py` | `[x]` |

---

### 190.3 Target Date Fund Rebalancing Calendar `[x]`

**Acceptance Criteria**: Predict Month-End and Quarter-End rebalancing flows.

| Component | File Path | Status |
|-----------|-----------|--------|
| Rebalance Predictor | `services/strategies/tdf_flow.py` | `[x]` |

---

### 190.4 CTAs (Trend Followers) Positioning Proxy `[x]`

**Acceptance Criteria**: Model Commodity Trading Advisors (CTAs).

| Component | File Path | Status |
|-----------|-----------|--------|
| CTA Modeler | `services/strategies/cta_positioning.py` | `[x]` |

---

### 190.5 Postgres Order Flow Toxicity Log `[x]`

**Acceptance Criteria**: Log "Toxic Flow" (VPIN metric).

| Component | File Path | Status |
|-----------|-----------|--------|
| Toxicity Calc | `services/market/toxicity_calc.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py liquidity check-risk-parity` | Est selling pressure | `[x]` |
| `python cli.py liquidity calc-vpin <ticker>` | Measure toxicity | `[x]` |

---

*Last verified: 2026-01-30*

