# Phase 77: Macro Regime Change Detector (Inflation/Deflation)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Macro Strategy Team

---

## 📋 Overview

**Description**: Detect major regime changes: Inflation vs Deflation. Rising Rates vs Falling Rates. These are decade-long trends. The portfolio must adapt structurally (e.g., Owning Gold in Inflation, Long Duration Bonds in Deflation).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 77

---

## 🎯 Sub-Deliverables

### 77.1 Regime Detection Algo (CPI/Rates ROC) `[ ]`

**Acceptance Criteria**: Analyze Rate of Change (ROC) of CPI and 10Y Yield. High Volatility in Rates = Regime Change.

| Component | File Path | Status |
|-----------|-----------|--------|
| Regime Algo | `services/analysis/regime_algo.py` | `[ ]` |

---

### 77.2 Structural Portfolio Allocator `[ ]`

**Acceptance Criteria**: Define "Structural" allocations. Inflation Regime = 20% Commodities. Deflation = 0% Commodities, 40% Bonds.

| Component | File Path | Status |
|-----------|-----------|--------|
| Allocator | `services/strategies/structural_alloc.py` | `[ ]` |

---

### 77.3 Historical Regime Overlay `[ ]`

**Acceptance Criteria**: Charting tool. Overlay 1970s (Stagflation) data onto current charts to spot fractals.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fractal Overlay | `frontend2/src/components/Charts/FractalMatch.jsx` | `[ ]` |

---

### 77.4 Breakeven Inflation Monitor (TIPS) `[ ]`

**Acceptance Criteria**: Monitor 5Y and 10Y Breakeven Inflation rates (Nominal - Real Yield). Best market predictor of inflation.

| Component | File Path | Status |
|-----------|-----------|--------|
| Breakeven Mon | `services/market/breakeven.py` | `[ ]` |

### 77.5 Fed Speak Sentiment Analysis `[ ]`

**Acceptance Criteria**: NLP on FOMC Minutes. "Hawkish" vs "Dovish" scoring.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fed NLP | `services/ai/fed_sentiment.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py regime status` | Infl/Defl | `[ ]` |
| `python cli.py regime compare-fractal` | 1970s correlation | `[ ]` |

---

*Last verified: 2026-01-25*
