# Phase 7: Fixed Income & Yield Curve Visualization

> **Phase 50** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Monitors the baseline cost of money (the 'Climate' of the Yellowstone ecosystem) to protect capital preservation layers.

---

## Overview

Comprehensive UI for managing bond ladders and analyzing the sovereign yield curve. Fixed income is the foundation of any institutional portfolio, and this phase provides the tools to monitor and manage this critical asset class.

---

## Sub-Deliverable 50.1: Bond Ladder Construction Interface

### Description
Visual drag-and-drop tool for planning staggered maturity schedules, allowing traders to construct optimal income streams.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/FixedIncome/BondLadder.jsx` | Main ladder widget |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/BondLadder.css` | Ladder styling |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/LadderRung.jsx` | Individual bond rung |
| `[NEW]` | `frontend2/src/stores/fixedIncomeStore.js` | Zustand store |
| `[NEW]` | `frontend2/src/hooks/useBondLadder.js` | Ladder logic hook |

### Verbose Acceptance Criteria

1. **Drag-and-Drop D3 Bars**
   - [ ] Vertical bar chart with years on Y-axis (1-30 years)
   - [ ] Draggable bars represent bond allocations per maturity year
   - [ ] Real-time updates to `useFixedIncomeStore` on drag
   - [ ] Snap-to-grid for clean alignment (1-year increments)

2. **Weighted Average Life (WAL) Calculation**
   - [ ] Display WAL prominently at top of widget
   - [ ] Formula: `WAL = Σ(Principal × Time) / Σ(Principal)`
   - [ ] Updates in real-time as bars are adjusted
   - [ ] Color indicator: Green (<5yr), Yellow (5-10yr), Red (>10yr)

3. **Liquidity Gap Indicators**
   - [ ] Visual warning icons for years with zero maturities
   - [ ] "Liquidity Gap Alert" when >2 consecutive years empty
   - [ ] Tooltip suggests optimal rebalancing

4. **Ladder Templates**
   - [ ] Pre-built templates: "Conservative", "Barbell", "Bullet"
   - [ ] One-click apply with confirmation modal
   - [ ] Save custom templates to user profile

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/fixed-income/ladder` | GET/POST | Retrieve/save ladder configuration |
| `/api/v1/fixed-income/templates` | GET | List available ladder templates |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BondLadder.test.jsx` | Renders all years, drag updates store, WAL calculates correctly |
| `LadderRung.test.jsx` | Drag events fire, snap-to-grid works |
| `fixedIncomeStore.test.js` | Store updates on changes, template apply works |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 50.2: Real-time Yield Curve (FRED API) Plotter

### Description
Interactive plotter for US Treasury curves with inversion detection, providing early warning of recession signals.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/FixedIncome/YieldCurve.jsx` | Yield curve chart |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/YieldCurve.css` | Chart styling |
| `[NEW]` | `frontend2/src/services/fredService.js` | FRED API integration |
| `[NEW]` | `frontend2/src/hooks/useYieldCurve.js` | Data fetching hook |

### Verbose Acceptance Criteria

1. **FRED API Integration**
   - [ ] Subscribe to Kafka topic `macro-fred-updates`
   - [ ] Latency monitoring: alert if lag >500ms
   - [ ] Fallback to REST API if Kafka unavailable
   - [ ] Cache last known values for offline display

2. **Curve Visualization**
   - [ ] D3.js line chart with maturities on X-axis (1M to 30Y)
   - [ ] Yields on Y-axis (0% to 8% range, auto-scaling)
   - [ ] Smooth curve interpolation (cubic spline)
   - [ ] Data points as circles on the curve

3. **Historical Animation**
   - [ ] Framer Motion animation showing curve shifts
   - [ ] Slider to scrub through 12-month historical window
   - [ ] "Play" button to animate curve evolution
   - [ ] Speed control: 1x, 2x, 5x

4. **Recession Signal Detection**
   - [ ] Monitor 10Y-2Y spread in real-time
   - [ ] "Recession Signal" alert banner when spread <0bps
   - [ ] Historical inversions marked on timeline
   - [ ] Link to educational explanation of yield curve inversion

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/macro/yield-curve` | GET | Current yield curve data |
| `/api/v1/macro/yield-curve/history` | GET | Historical yield curves |
| `/ws/macro-updates` | WS | Real-time macro data stream |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `YieldCurve.test.jsx` | Renders curve, handles missing data, inversion alert shows |
| `fredService.test.js` | API calls work, caching logic, fallback behavior |
| `useYieldCurve.test.js` | Subscribes to updates, handles errors |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 50.3: Duration & Convexity Risk Gauges

### Description
High-fidelity gauges showing portfolio sensitivity to interest rate oscillations, critical for managing fixed income risk.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/FixedIncome/DurationGauges.jsx` | Dual gauge widget |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/DurationGauges.css` | Gauge styling |
| `[NEW]` | `frontend2/src/components/Gauges/SemiCircularGauge.jsx` | Reusable gauge |

### Verbose Acceptance Criteria

1. **Rate Shock Sensitivity**
   - [ ] Display sensitivity to +/- 100bps rate shock
   - [ ] Show dollar impact: "+100bps = -$X,XXX"
   - [ ] Color-coded impact: Green (<2% loss), Yellow (2-5%), Red (>5%)

2. **Duration Gauge**
   - [ ] Semi-circular gauge (0-20 years range)
   - [ ] Current portfolio duration as needle
   - [ ] Target zone indicator (user-configurable)
   - [ ] "Modified Duration" and "Macaulay Duration" toggle

3. **Convexity Gauge**
   - [ ] Separate gauge for convexity measure
   - [ ] "Stress Zone" highlight when convexity becomes negative
   - [ ] Negative convexity = accelerating losses, requires warning
   - [ ] Tooltip explaining convexity impact

4. **Data Verification**
   - [ ] Data source validated against Postgres time-series tables
   - [ ] "Data Quality" indicator: Green/Yellow/Red
   - [ ] Last update timestamp prominently displayed

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DurationGauges.test.jsx` | Both gauges render, shock calculation correct |
| `SemiCircularGauge.test.jsx` | Needle position, color zones, tooltip |

### Test Coverage Target: **80%**

---

## Widget Registry Entries

```javascript
{
  id: 'bond-ladder',
  name: 'Bond Ladder Builder',
  component: lazy(() => import('../../widgets/FixedIncome/BondLadder')),
  category: 'Fixed Income',
  defaultSize: { width: 450, height: 500 }
},
{
  id: 'yield-curve',
  name: 'Treasury Yield Curve',
  component: lazy(() => import('../../widgets/FixedIncome/YieldCurve')),
  category: 'Fixed Income',
  defaultSize: { width: 600, height: 350 }
},
{
  id: 'duration-gauges',
  name: 'Duration & Convexity',
  component: lazy(() => import('../../widgets/FixedIncome/DurationGauges')),
  category: 'Fixed Income',
  defaultSize: { width: 400, height: 300 }
}
```

---

## Route Integration

**Route:** `/strategist/fixed-income`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

