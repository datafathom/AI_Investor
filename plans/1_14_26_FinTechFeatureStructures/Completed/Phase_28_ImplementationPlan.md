# Phase 28: Retail 'BS' Noise Filter Implementation

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Purge standard retail indicators (RSI, Moving Average Crossovers, Head & Shoulders) from the agent data stream. Focusing on "Institutional Alpha" requires ignoring the noise that retail traders look at, or using it as a contrarian signal.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 28

---

## 🎯 Sub-Deliverables

### 28.1 Indicator Purge from SearcherAgent `[x]`

**Acceptance Criteria**: Systematically remove all MA Crossover and RSI modules from SearcherAgent. Verify code removal/disablement.

| Component | File Path | Status |
|-----------|-----------|--------|
| Cleanup Script | `scripts/cleanup/remove_retail_logic.py` | `[x]` |

---

### 28.2 Retail Pattern Ignore List `[x]`

**Acceptance Criteria**: Ensure that 'Head & Shoulders' and standard retail trendline patterns are explicitly ignored (or not calculated at all).

| Component | File Path | Status |
|-----------|-----------|--------|
| Config | `config/indicators/ignore_list.json` | `[x]` |

---

### 28.3 Low Volume Session Suppressor `[x]`

**Acceptance Criteria**: Implement a noise suppression module that filters out signals originating in 'Low Volume' retail sessions (e.g., Asian lunch hour for EUR/USD). Focus on London/NY overlaps.

```python
class TimeSessionFilter:
    def is_institutional_session(self, timestamp: datetime) -> bool:
        # Allow London (3AM-11AM EST) and NY (8AM-5PM EST)
        # Block Asia late hours
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Session Filter | `services/market/session_filter.py` | `[x]` |

---

### 28.4 Institutional Primitive Enforcer (GEX) `[x]`

**Acceptance Criteria**: Configure SearcherAgent to act *only* on institutional 'GEX' (Gamma Exposure) and 'Order Block' logic.

| Component | File Path | Status |
|-----------|-----------|--------|
| GEX Integration | `services/indicators/gex_feed.py` | `[x]` |

---

### 28.5 'Suppressed Signal' Log `[x]`

**Acceptance Criteria**: Log every signal that *would* have been taken by a retail strat but was rejected, to prove the value of the filter (Backtest: "Retail vs Institutional").

| Component | File Path | Status |
|-----------|-----------|--------|
| Suppression Log | `services/logging/suppression_log.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py filter check-signal` | Is signal retail BS? | `[x]` |
| `python cli.py filter list-blocked` | Show rejected signals | `[x]` |

---

*Last verified: 2026-01-25*
