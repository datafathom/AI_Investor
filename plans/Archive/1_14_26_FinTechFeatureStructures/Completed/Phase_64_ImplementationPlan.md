# Phase 64: Gamma Exposure (GEX) Engine

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Ingest and calculate Gamma Exposure (GEX). When Market Makers are short gamma, they must hedge by selling into weakness (accelerating crashes) or buying into strength (accelerating pumps). This indicates volatility regimes.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 64

---

## 🎯 Sub-Deliverables

### 64.1 Options Chain Ingestion (SPX/QQQ) `[x]`

**Acceptance Criteria**: Ingest full option chains (Open Interest, Volume, Delta, Gamma) for SPX and QQQ.

| Component | File Path | Status |
|-----------|-----------|--------|
| Ingestor | `services/ingestion/options_chain.py` | `[x]` |

---

### 64.2 Net GEX Calculator `[x]`

**Acceptance Criteria**: Calculate Net GEX (Call Gamma - Put Gamma) for every strike.
`GEX = OI * Gamma * Spot * 100`.

```python
class GEXCalculator:
    def calculate_total_gex(self, chain):
        return sum(call.gamma * call.oi) - sum(put.gamma * put.oi)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| GEX Engine | `services/analysis/gex_calc.py` | `[x]` |

---

### 64.3 Zero Gamma Level Detection `[x]`

**Acceptance Criteria**: Identify the "Zero Gamma" level (Flip Point). Above = Low Volatility (Mean Reverting). Below = High Volatility (Directional).

| Component | File Path | Status |
|-----------|-----------|--------|
| Flip Detector | `services/analysis/zero_gamma.py` | `[x]` |

---

### 64.4 Volatility Regime Flag `[x]`

**Acceptance Criteria**: Set system `VOL_REGIME` based on GEX. Positive GEX -> Enable Mean Reversion Strats. Negative GEX -> Enable Trend Following / Hedging.

| Component | File Path | Status |
|-----------|-----------|--------|
| Regime Setter | `services/modes/gex_regime.py` | `[x]` |

### 64.5 GEX Profile Visualization `[x]`

**Acceptance Criteria**: Visual chart showing GEX bars at each strike price. "Where is the Gamma Wall?"

| Component | File Path | Status |
|-----------|-----------|--------|
| Chart | `frontend2/src/components/Charts/GEXProfile.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py gex profile <ticker>` | Show gamma walls | `[x]` |
| `python cli.py gex check-flip` | Find zero level | `[x]` |

---

*Last verified: 2026-01-25*
