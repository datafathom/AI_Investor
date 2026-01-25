# Phase 14: Advanced Backtest Result Explorer (V2)

> **Phase 57** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Uses 10,000 parallel realities to ensure the current strategy is not an outlier and avoids extinction.

---

## Overview

Deep-dive statistical explorer for historical simulation results with Monte Carlo analysis.

---

## Sub-Deliverable 57.1: Monte Carlo Simulation Path Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/MonteCarlo.jsx` | Main visualizer |
| `[NEW]` | `frontend2/src/widgets/Backtest/MonteCarlo.css` | Styling |
| `[NEW]` | `frontend2/src/hooks/useMonteCarloSim.js` | Simulation hook |
| `[NEW]` | `frontend2/src/workers/monteCarlo.worker.js` | Web Worker |

### Verbose Acceptance Criteria

1. **HTML5 Canvas 10K Path Rendering**
   - [ ] Render 10,000 potential future equity paths
   - [ ] Maintain 60 FPS during pan/zoom
   - [ ] Use Web Worker for calculation (non-blocking)
   - [ ] Progressive rendering: show paths as calculated

2. **Quantile Shading**
   - [ ] 5th percentile (worst case) - dark red fill
   - [ ] 50th percentile (median) - solid line
   - [ ] 95th percentile (best case) - dark green fill
   - [ ] Shaded area between quantiles

3. **Probability of Ruin**
   - [ ] Calculate based on user-defined drawdown limits
   - [ ] Default limit: 25% drawdown = ruin
   - [ ] Display as percentage: "3.2% Probability of Ruin"
   - [ ] Red warning if >5% probability

4. **Interactive Volatility Slider**
   - [ ] Adjust volatility assumptions in real-time
   - [ ] See path distribution shift instantly
   - [ ] Presets: Historical Vol, 1.5x Historical, 2x Historical
   - [ ] Custom input option

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/backtest/monte-carlo` | POST | Run simulation with parameters |
| `/api/v1/backtest/paths` | GET | Pre-computed path data |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `MonteCarlo.test.jsx` | Canvas renders, paths visible, slider updates |
| `useMonteCarloSim.test.js` | Simulation parameters, worker communication |
| `monteCarlo.worker.test.js` | Path calculation, quantile accuracy |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 57.2: Maximum Drawdown 'Stress Point' Timeline

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/DrawdownTimeline.jsx` | Timeline widget |
| `[NEW]` | `frontend2/src/widgets/Backtest/DrawdownTimeline.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Backtest/UnderwaterChart.jsx` | Underwater view |

### Verbose Acceptance Criteria

1. **Neo4j Macro Event Annotations**
   - [ ] Link drawdown periods to `MACRO_EVENT` nodes
   - [ ] Example annotations: "2020 COVID Crash", "2022 Fed Hikes"
   - [ ] Click annotation to view event details
   - [ ] Custom annotation support

2. **Underwater Chart**
   - [ ] Inverted chart showing time spent below peak
   - [ ] Calculate time-to-recovery for each dip
   - [ ] Color intensity by drawdown severity
   - [ ] Longest underwater period highlighted

3. **Risk Metrics**
   - [ ] Calculate Ulcer Index (RMS of drawdowns)
   - [ ] Calculate Pain Index (mean of drawdowns)
   - [ ] Compare to benchmark metrics
   - [ ] "Strategy Risk Rating" composite score

4. **Timeline Navigation**
   - [ ] Horizontal timeline with zoom
   - [ ] Click event to see strategy performance during crisis
   - [ ] Compare multiple strategies side-by-side

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DrawdownTimeline.test.jsx` | Timeline renders, annotations clickable |
| `UnderwaterChart.test.jsx` | Chart displays, recovery calculation |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 57.3: Out-of-Sample Performance Variance Matrix

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/OverfitWarning.jsx` | Variance matrix |
| `[NEW]` | `frontend2/src/widgets/Backtest/OverfitWarning.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Backtest/MetricComparison.jsx` | Metric table |

### Verbose Acceptance Criteria

1. **Overfit Detection**
   - [ ] Visual "Overfit Warning" if IS/OOS variance >20%
   - [ ] Warning banner with explanation
   - [ ] Variance calculation methodology displayed
   - [ ] Suggestions for reducing overfit

2. **Metric Comparison per Year**
   - [ ] Sharpe ratio per yearly bucket
   - [ ] Sortino ratio per yearly bucket
   - [ ] Side-by-side In-Sample vs Out-of-Sample
   - [ ] Color coding: Green (consistent), Red (divergent)

3. **Zustand Persistence for Sharing**
   - [ ] Save backtest parameters to Zustand store
   - [ ] Generate shareable URL with encoded parameters
   - [ ] One-click "Share Results" button
   - [ ] Import from shared URL

4. **Statistical Tests**
   - [ ] Run t-test for IS/OOS difference
   - [ ] P-value display with significance indicator
   - [ ] Confidence interval for expected returns

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `OverfitWarning.test.jsx` | Warning displays at threshold, metrics table |
| `MetricComparison.test.jsx` | Years render, color coding correct |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/analyst/backtest`

**Macro Task:** The Analyst

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

