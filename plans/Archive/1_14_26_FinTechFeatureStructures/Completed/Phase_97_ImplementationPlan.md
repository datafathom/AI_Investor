# Phase 97: Central Bank Liquidity Visualizer

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Macro Strategy Team

---

## 📋 Overview

**Description**: "Don't fight the Fed." Track Net Liquidity (Fed Balance Sheet - TGA - RRP). When Net Liq rises, Stocks rise.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 97

---

## 🎯 Sub-Deliverables

### 97.1 Fed Balance Sheet Ingest `[x]`

**Acceptance Criteria**: Weekly H.4.1 release. Total Assets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fed Assets | `services/ingestion/fed_balance.py` | `[x]` |

---

### 97.2 TGA (Treasury General Account) `[x]`

**Acceptance Criteria**: Checking account of the Treasury. When TGA goes UP, Liquidity goes DOWN (bad for stocks).

| Component | File Path | Status |
|-----------|-----------|--------|
| TGA Track | `services/market/tga_level.py` | `[x]` |

---

### 97.3 Reverse Repo (RRP) Facility `[x]`

**Acceptance Criteria**: Daily RRP usage. Cash parked at Fed. RRP down = Liquidity injected into market.

| Component | File Path | Status |
|-----------|-----------|--------|
| RRP Track | `services/market/rrp_level.py` | `[x]` |

---

### 97.4 Net Liquidity Equation Chart `[x]`

**Acceptance Criteria**: Chart `Net Liq = Bal Sheet - TGA - RRP`. Overlay SPX. 95% Correlation.

| Component | File Path | Status |
|-----------|-----------|--------|
| Net Liq Chart | `frontend2/src/components/Macro/NetLiquidity.jsx` | `[x]` |

### 97.5 Global Central Bank Injection `[x]`

**Acceptance Criteria**: Add ECB + BOJ + PBOC balance sheets. Global M2 measure.

| Component | File Path | Status |
|-----------|-----------|--------|
| Global M2 | `services/analysis/global_m2.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py liquidity net` | Current Net Liq | `[x]` |
| `python cli.py liquidity global` | Total M2 | `[x]` |

---

*Last verified: 2026-01-25*
