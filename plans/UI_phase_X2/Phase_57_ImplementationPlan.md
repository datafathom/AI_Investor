# Phase 57: Advanced Backtest Result Explorer (V2)

> **Phase ID**: 57 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Uses 10,000 parallel realities to ensure the current strategy is not an outlier and avoids extinction.

---

## Overview

Deep-dive statistical explorer for historical simulation results.

---

## Sub-Deliverable 57.1: Monte Carlo Simulation Path Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/MonteCarloViz.jsx` | Canvas-based paths |
| `[NEW]` | `frontend2/src/widgets/Backtest/MonteCarloViz.css` | Styling |
| `[MODIFY]` | `frontend2/src/stores/backtestStore.js` | Enhanced state |
| `[NEW]` | `services/analysis/monte_carlo_service.py` | GBM simulation |
| `[MODIFY]` | `web/api/backtest_api.py` | Enhanced endpoints |

### Verbose Acceptance Criteria

1. **10k Path Rendering**
   - [ ] HTML5 Canvas at 60 FPS
   - [ ] Quantile shading (5/50/95%)
   - [ ] Geometric Brownian Motion (GBM)

2. **Probability of Ruin**
   - [ ] Based on user-defined drawdown limits
   - [ ] Visual 'Extinction Event' marker
   - [ ] Percentage display

3. **Interactive Sliders**
   - [ ] Adjust volatility (sigma) in real-time
   - [ ] Adjust drift (mu) in real-time
   - [ ] See path shifts instantly

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `MonteCarloViz.test.jsx` | Paths render, quantiles display, sliders work |
| `backtestStore.test.js` | Simulation params persist |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_monte_carlo_service.py` | `test_gbm_simulation`, `test_ruin_probability`, `test_quantile_calculation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 57.2: Maximum Drawdown 'Stress Point' Timeline

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/DrawdownTimeline.jsx` | Annotated timeline |
| `[NEW]` | `frontend2/src/widgets/Backtest/DrawdownTimeline.css` | Styling |

### Verbose Acceptance Criteria

1. **Event Annotations**
   - [ ] Link to `MACRO_EVENT` nodes in Neo4j
   - [ ] '2020 C19 Crash', '2008 Financial Crisis' labels
   - [ ] Clickable for details

2. **Underwater Chart**
   - [ ] Time-to-recovery in days
   - [ ] Depth visualization
   - [ ] Current vs historical comparison

3. **Risk Metrics**
   - [ ] Ulcer Index calculation
   - [ ] Pain Index (duration × depth)
   - [ ] Rolling max drawdown

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DrawdownTimeline.test.jsx` | Timeline renders, events annotated, metrics display |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_monte_carlo_service.py` | `test_drawdown_calculation`, `test_ulcer_index`, `test_recovery_time` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 57.3: Out-of-Sample Performance Variance Matrix

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/VarianceMatrix.jsx` | Overfit detector |
| `[NEW]` | `frontend2/src/widgets/Backtest/VarianceMatrix.css` | Styling |

### Verbose Acceptance Criteria

1. **Overfit Warning**
   - [ ] Visual alert if IS vs OOS Sharpe variance > 20%
   - [ ] Red border warning
   - [ ] Explanation tooltip

2. **Ratio Comparison**
   - [ ] Sharpe, Sortino, Calmar per yearly bucket
   - [ ] Side-by-side table
   - [ ] Historical trend lines

3. **Parameter Sharing**
   - [ ] Zustand persistence for backtest params
   - [ ] Easy sharing across agent swarms
   - [ ] URL-encoded params

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `VarianceMatrix.test.jsx` | Matrix renders, overfit warning, ratio comparison |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_monte_carlo_service.py` | `test_sharpe_calculation`, `test_overfit_detection`, `test_param_serialization` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/analyst/backtest`

**Macro Task:** Robustness Verification

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Backtest

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_monte_carlo_service.py -v --cov=services/analysis
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/analyst/backtest
# Verify: 10k paths render smoothly, drawdown annotated, overfit detector works
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 57 detailed implementation plan |
