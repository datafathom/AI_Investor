# Phase 24: Real-Estate & Illiquid Asset Tracking + Zen Mode

> **Phases 67-68** | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Verification: Verified via browser (Screenshots: `Phase_24_Assets_Dashboard.png`, `Phase_24_Zen_Mode.png`)
> Strategic Importance: Incorporates 'Slow Capital' into the high-frequency Net Worth model and enables the ultimate goal of 'Enough'.

---

## Overview

Tracking of physical assets and the final Zen Mode for long-term peace of mind.

---

## Sub-Deliverable 67.1: Manual Asset Entry (Physical Property, Art, Private Equity)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/ManualEntry.jsx` | Entry form |
| `[NEW]` | `frontend2/src/widgets/Assets/ManualEntry.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Assets/AssetCategories.jsx` | Category picker |
| `[NEW]` | `frontend2/src/stores/wealthStore.js` | Total wealth state |

### Verbose Acceptance Criteria

1. **Neo4j Entity Tax Mapping**
   - [ ] Link assets to `ENTITY` nodes
   - [ ] Tax implications per entity type
   - [ ] Ownership percentage tracking
   - [ ] Multi-entity ownership support

2. **Document Upload Integration**
   - [ ] Upload appraisals and insurance documents
   - [ ] Link to Document Vault
   - [ ] "Missing Document" warnings
   - [ ] Expiration tracking for appraisals

3. **TotalWealth Zustand Merge**
   - [ ] Merge liquid and illiquid assets into single slice
   - [ ] Calculate combined Net Worth
   - [ ] Update on any asset change
   - [ ] Separate view toggle: Liquid/Illiquid/All

4. **Asset Categories**
   - [ ] Real Estate (Primary, Rental, Vacation)
   - [ ] Art & Collectibles
   - [ ] Private Equity/Venture
   - [ ] Vehicles & Personal Property

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ManualEntry.test.jsx` | Form submission, validation |
| `AssetCategories.test.jsx` | Category display, selection |
| `wealthStore.test.js` | Merge logic, total calculation |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 67.2: Estimated Valuation Depreciation/Appreciation Slider

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/ValuationSlider.jsx` | Slider widget |
| `[NEW]` | `frontend2/src/widgets/Assets/ValuationSlider.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Assets/ValueHistory.jsx` | Historical chart |

### Verbose Acceptance Criteria

1. **Real-time Net Worth Impact**
   - [ ] Net Worth updates as slider moves
   - [ ] Delta display: "+$50,000 (↑2.1%)"
   - [ ] Undo/reset to original estimate
   - [ ] Save new estimate

2. **Zillow/Redfin Integration**
   - [ ] API integration for property estimates
   - [ ] "Zestimate" display
   - [ ] Compare to manual valuation
   - [ ] Auto-update option

3. **Historical Value Timeline**
   - [ ] Chart showing value over time
   - [ ] Entry points for manual updates
   - [ ] Appreciation rate calculation
   - [ ] Compare to inflation

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ValuationSlider.test.jsx` | Slider movement, impact calculation |
| `ValueHistory.test.jsx` | Timeline display, data points |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 67.3: Unified Wealth 'Net Worth' Circular Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/NetWorthGauges.jsx` | Gauge widget |
| `[NEW]` | `frontend2/src/widgets/Assets/NetWorthGauges.css` | Styling |

### Verbose Acceptance Criteria

1. **D3.js Dual-Ring Visualization**
   - [ ] Inner ring: Liquid assets (Stocks, Crypto, Cash)
   - [ ] Outer ring: Illiquid assets (Real Estate, PE, Art)
   - [ ] Ring segments by category
   - [ ] Color-coded by asset class

2. **Center Net Worth Display**
   - [ ] Total Net Worth prominently displayed
   - [ ] 24h change with delta
   - [ ] Sparkline of recent trend
   - [ ] "All-Time High" badge if applicable

3. **Framer Motion Load Animation**
   - [ ] Rings animate on dashboard load
   - [ ] Smooth segment transitions on data change
   - [ ] Hover to expand segment details
   - [ ] Click for full breakdown

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `NetWorthGauges.test.jsx` | Rings render, center display, animation |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.1: Minimalist Goal Tracking UI (The 'Enough' Metric)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/pages/ZenMode.jsx` | Zen mode page |
| `[NEW]` | `frontend2/src/pages/ZenMode.css` | Zen styling |
| `[NEW]` | `frontend2/src/widgets/Zen/GoalProgress.jsx` | Progress bar |

### Verbose Acceptance Criteria

1. **Hide High-Frequency Noise**
   - [ ] Hide all price charts
   - [ ] No red/green flash indicators
   - [ ] Calm, muted color palette
   - [ ] Slow, deliberate animations

2. **Freedom Number Progress**
   - [ ] Simple progress bar to "Freedom Number"
   - [ ] "Glow" effect when goal reached
   - [ ] Percentage complete
   - [ ] "You're 73% to Enough"

3. **Income vs Expenses Focus**
   - [ ] "Projected Annual Income" from portfolio
   - [ ] vs "Annual Expenses" (user-defined)
   - [ ] "Covered: X years of expenses"
   - [ ] Monthly income breakdown

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ZenMode.test.jsx` | Mode renders, no flashy elements |
| `GoalProgress.test.jsx` | Progress bar, glow effect |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.2: Time-to-Retirement Countdown & Probability Gauge

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Zen/RetirementGauge.jsx` | Countdown gauge |
| `[NEW]` | `frontend2/src/widgets/Zen/RetirementGauge.css` | Styling |

### Verbose Acceptance Criteria

1. **Monte Carlo Survival Probability**
   - [ ] Simulation of retirement scenarios
   - [ ] Target: >99% success probability
   - [ ] Visual gauge showing probability
   - [ ] Red warning if <90%

2. **Safety Buffer Display**
   - [ ] "X years of expenses covered"
   - [ ] Based on current portfolio value
   - [ ] Adjusts for inflation
   - [ ] Best/worst case scenarios

3. **Lifestyle Toggle**
   - [ ] Zustand-based "Frugal vs Lux" toggle
   - [ ] Adjusts expense assumptions
   - [ ] Re-calculates immediately
   - [ ] Compare side-by-side

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `RetirementGauge.test.jsx` | Probability display, toggle works |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.3: System Autopilot Master Override (The 'Peace of Mind' Toggle)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Zen/AutopilotToggle.jsx` | Autopilot widget |
| `[NEW]` | `frontend2/src/widgets/Zen/AutopilotToggle.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Zen/HomeostasisOverlay.jsx` | Zen overlay |

### Verbose Acceptance Criteria

1. **Disable High-Frequency Consumers**
   - [ ] Disable all high-frequency Kafka consumers
   - [ ] Agents shift to dividend-seeking logic
   - [ ] No active trading
   - [ ] Preserves capital

2. **Lock Manual Trading**
   - [ ] Lock out manual trading buttons
   - [ ] Prevent emotional intervention
   - [ ] Require re-authentication to unlock
   - [ ] Cool-down period

3. **Homeostatic Display**
   - [ ] "System Homeostatic" message
   - [ ] Backdrop-blur with slow-moving particles
   - [ ] Calming ambient visual
   - [ ] Sound option (nature sounds)

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `AutopilotToggle.test.jsx` | Toggle state, lock behavior |
| `HomeostasisOverlay.test.jsx` | Overlay renders, particle animation |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/zen`

**Macro Task:** Homeostasis

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan - combined 67+68 as final phase |

