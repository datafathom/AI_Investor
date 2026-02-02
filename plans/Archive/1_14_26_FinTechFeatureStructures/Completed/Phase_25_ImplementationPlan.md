# Phase 25: Risk-Reward vs. Probability Edge Comparison

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Deploy analytical tools to compare the mathematical expectancy of the system's survival architectures. Specifically, prove that High Risk-Reward (3:1) with Low Win Rate (40%) is superior to High Win Rate (90%) with Inverse Risk-Reward (1:10, risking $10 to make $1).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 25

---

## 🎯 Sub-Deliverables

### 25.1 'Peter Lynch Legend' Metric (60% Baseline) `[x]`

**Acceptance Criteria**: Implement a metric calculating the portfolio's deviation from a theoretical "Legend" standard (60% win rate, 2:1 RR).

| Component | File Path | Status |
|-----------|-----------|--------|
| Metric Calculator | `services/analysis/lynch_metric.py` | `[x]` |

---

### 25.2 Expectancy Calculator (RR vs WinRate) `[x]`

**Acceptance Criteria**: Calculate mathematical expectancy: `(Win % * Avg Win) - (Loss % * Avg Loss)`. Display prominently.

```python
class ExpectancyEngine:
    def calculate(self, results: list[Trade]) -> float:
        win_rate = win_count / total
        avg_win = sum(wins) / win_count
        avg_loss = sum(losses) / loss_count
        return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Expectancy Engine | `services/analysis/expectancy_engine.py` | `[x]` |

---

### 25.3 Periodic Survival Scorecard Generator `[x]`

**Acceptance Criteria**: Generate monthly 'Survival Scorecards' based on R-Multiple consistency and drawdown duration (not just profit).

| Component | File Path | Status |
|-----------|-----------|--------|
| Scorecard Gen | `services/reporting/survival_score.py` | `[x]` |

---

### 25.4 Alpha Attribution (Luck vs. Edge) `[x]`

**Acceptance Criteria**: Statistical test. Was the profit from one lucky 20R trade, or consistent 2R trades? Cap outlier wins in "Adjusted Expectancy" to see base skill.

| Component | File Path | Status |
|-----------|-----------|--------|
| Attribution | `services/analysis/alpha_attributor.py` | `[x]` |

---

### 25.5 Monte Carlo Projection of Current Stats `[x]`

**Acceptance Criteria**: Project current win-rate/RR forward 1000 trades to check for "Ruin" probability.

| Component | File Path | Status |
|-----------|-----------|--------|
| Projection Sim | `services/simulation/monte_carlo_sim.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Expectancy Chart | `frontend2/src/components/Analysis/ExpectancyCurve.jsx` | `[x]` |
| Edge Dashboard | `frontend2/src/components/Analysis/EdgeDash.jsx` | `[x]` |

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py stats calc-expectancy` | Run math | `[x]` |
| `python cli.py stats verify-edge` | Run Monte Carlo | `[x]` |

---

*Last verified: 2026-01-25*
