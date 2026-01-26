# Phase 99: Quantamental Integration (Tech + Macro + Fund)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: The Holy Grail. Combine Technicals (Searcher), Macro (Warden), and Fundamentals (Value). A signal is only valid if ALL THREE agree. "Triple Confluence".

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 99

---

## 🎯 Sub-Deliverables

### 99.1 Triple Confluence Signal Engine `[ ]`

**Acceptance Criteria**: `Signal = Tech_Score + Macro_Score + Fund_Score`. Threshold > 80/100 to buy.

```python
class ConfluenceEngine:
    def score(self, ticker):
        tech = self.searcher.get_score(ticker)
        fund = self.value.get_score(ticker)
        macro = self.warden.get_regime_score()
        return (tech + fund + macro) / 3
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Engine | `services/strategies/confluence.py` | `[ ]` |

---

### 99.2 Unified Scoring Database `[ ]`

**Acceptance Criteria**: Table storing component scores for every asset daily.

| Component | File Path | Status |
|-----------|-----------|--------|
| Score DB | `services/storage/daily_scores.py` | `[ ]` |

---

### 99.3 Disagreement Analyzer `[ ]`

**Acceptance Criteria**: What if Tech says Buy, but Macro says Crash? Implement rules for conflict resolution (usually Macro wins).

| Component | File Path | Status |
|-----------|-----------|--------|
| Arbitrator | `services/strategies/conflict_res.py` | `[ ]` |

---

### 99.4 'Perfect Setup' Screener `[ ]`

**Acceptance Criteria**: Screen for 99/100 scores. "Perfect Storm" trades.

| Component | File Path | Status |
|-----------|-----------|--------|
| Screener | `frontend2/src/components/Research/PerfectSetup.jsx` | `[ ]` |

### 99.5 Quantamental Backtest `[ ]`

**Acceptance Criteria**: Verify that Triple Confluence performs better than any single strategy alone.

| Component | File Path | Status |
|-----------|-----------|--------|
| Backtest | `services/backtest/triple_conf.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py confluence check <ticker>` | Get 3 scores | `[ ]` |
| `python cli.py confluence find-best` | Top picks | `[ ]` |

---

*Last verified: 2026-01-25*
