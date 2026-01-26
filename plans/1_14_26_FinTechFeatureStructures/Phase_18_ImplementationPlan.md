# Phase 18: The R-Multiple Performance Engine

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Shift performance tracking from win-rate frequency to the magnitude of wins using the R-Multiple framework (2R, 5R, 10R).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 18.1 R (Initial Risk) Calculation `[ ]`

**Acceptance Criteria**: Implement logic to calculate the 'R' (Initial Risk Amount) for every position at the moment of entry.

| Component | File Path | Status |
|-----------|-----------|--------|
| R Calculator | `services/performance/r_calculator.py` | `[ ]` |
| Entry Analyzer | `services/performance/entry_analyzer.py` | `[ ]` |

---

### 18.2 Real-time R-Multiple Display `[ ]`

**Acceptance Criteria**: Configure the GUI to display real-time R-Multiple tracking for open trades (e.g., 'Currently +2.4R').

| Component | File Path | Status |
|-----------|-----------|--------|
| R-Multiple Widget | `frontend2/src/components/RMultipleWidget.jsx` | `[ ]` |
| Trade Card | `frontend2/src/components/TradeCard.jsx` | `[ ]` |

---

### 18.3 R-Multiple Distribution Dashboard `[ ]`

**Acceptance Criteria**: Verify that the performance dashboard prioritizes R-Multiple distribution over win-rate percentage.

| Component | File Path | Status |
|-----------|-----------|--------|
| Distribution Chart | `frontend2/src/components/RDistributionChart.jsx` | `[ ]` |
| Performance Page | `frontend2/src/pages/PerformanceDashboard.jsx` | `[ ]` |

---

### 18.4 Agent R-Multiple Statistics `[ ]`

**Acceptance Criteria**: Implement statistical reporting that identifies which agent personas generate the highest average R-Multiples.

| Component | File Path | Status |
|-----------|-----------|--------|
| Agent Stats Service | `services/performance/agent_stats.py` | `[ ]` |
| Leaderboard API | `web/api/performance/leaderboard.py` | `[ ]` |

---

### 18.5 Trade Journal R-Multiple Sorting `[ ]`

**Acceptance Criteria**: Sort the trade journal by R-Multiple to highlight 'Big Winners' and analyze their logic-based TA primitives.

| Component | File Path | Status |
|-----------|-----------|--------|
| Journal Sorter | `services/journal/r_sorter.py` | `[ ]` |
| Big Winners Analyzer | `services/performance/big_winners.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 18.1 R Calculation | `[ ]` | `[ ]` |
| 18.2 Real-time Display | `[ ]` | `[ ]` |
| 18.3 Distribution Dashboard | `[ ]` | `[ ]` |
| 18.4 Agent Statistics | `[ ]` | `[ ]` |
| 18.5 Journal Sorting | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
