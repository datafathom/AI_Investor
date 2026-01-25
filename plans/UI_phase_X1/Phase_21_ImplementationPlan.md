# Phase 21: Advanced Margin & Collateral Management

> **Phase 64** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Prevents the 'Starvation' event of a margin call which leads to ecosystem collapse.

---

## Overview

Precision monitoring of buying power and liquidation risk to prevent forced selling.

---

## Sub-Deliverable 64.1: Maintenance Margin 'Danger Zone' Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/DangerZone.jsx` | Danger gauge |
| `[NEW]` | `frontend2/src/widgets/Margin/DangerZone.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Margin/PositionRisk.jsx` | Per-position risk |
| `[NEW]` | `frontend2/src/stores/riskStore.js` | Risk state store |

### Verbose Acceptance Criteria

1. **D3.js Linear Gauge**
   - [ ] Visual gauge showing proximity to margin call
   - [ ] Zones: Safe (green), Caution (yellow), Danger (red)
   - [ ] Current margin usage percentage
   - [ ] Maintenance margin requirement line

2. **Distance to Liquidate**
   - [ ] Calculate % drop to trigger liquidation per position
   - [ ] Top 5 most leveraged positions highlighted
   - [ ] "AAPL: 12.3% drop triggers liquidation"
   - [ ] Sort by risk level

3. **15% Buffer Alert**
   - [ ] Visual red pulse when margin buffer <15%
   - [ ] Push notification optional
   - [ ] Sound alert (configurable)
   - [ ] "Add Cash" or "Close Position" CTAs

4. **useRiskStore Integration**
   - [ ] Real-time collateral revaluation
   - [ ] Update on every price tick
   - [ ] Historical margin usage chart
   - [ ] Peak margin usage marker

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/margin/status` | GET | Current margin metrics |
| `/api/v1/margin/liquidation-risk` | GET | Per-position risk |
| `/ws/margin-updates` | WS | Real-time updates |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DangerZone.test.jsx` | Gauge renders, zones correct, pulse animation |
| `PositionRisk.test.jsx` | Risk calculation, sorting |
| `riskStore.test.js` | State updates, threshold triggers |

### Test Coverage Target: **90%** (margin-critical)

---

## Sub-Deliverable 64.2: Cross-Collateralization Asset Priority Toggle

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/CollateralPriority.jsx` | Priority widget |
| `[NEW]` | `frontend2/src/widgets/Margin/CollateralPriority.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Margin/LiquidationHierarchy.jsx` | Hierarchy builder |

### Verbose Acceptance Criteria

1. **Drag-and-Drop Liquidation Hierarchy**
   - [ ] Ordered list of assets to sell first
   - [ ] Drag to reorder priority
   - [ ] "Sell First" → "Sell Last" ordering
   - [ ] Save preferences to backend

2. **Margin Impact Calculator**
   - [ ] Calculate impact of selling each asset
   - [ ] "Selling AAPL releases $5,000 margin"
   - [ ] Optimal sell order suggestion
   - [ ] Consider tax implications

3. **Protected Assets Indicator**
   - [ ] "Lock" icon for core long-term holdings
   - [ ] Protected assets sold last
   - [ ] Require confirmation to unlock
   - [ ] Override in emergency only

4. **What-If Simulator**
   - [ ] Simulate selling specific assets
   - [ ] Show resulting margin health
   - [ ] Compare scenarios
   - [ ] "Optimize" auto-suggest

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CollateralPriority.test.jsx` | Drag-and-drop, save state |
| `LiquidationHierarchy.test.jsx` | Order display, lock toggle |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 64.3: Automated Margin Call Liquidation Order Editor

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/LiquidationEditor.jsx` | Editor widget |
| `[NEW]` | `frontend2/src/widgets/Margin/LiquidationEditor.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Margin/GhostOrder.jsx` | Preview order |

### Verbose Acceptance Criteria

1. **Ghost Order Visualization**
   - [ ] "Ghost Order" showing broker's intended liquidation
   - [ ] Based on your priority settings or broker default
   - [ ] Order book sweep simulation
   - [ ] Impact on remaining positions

2. **Expected Slippage Display**
   - [ ] Calculate slippage for forced liquidation
   - [ ] Compare to normal market hours execution
   - [ ] "Worst case: $X,XXX slippage"
   - [ ] Historical slippage data

3. **One-Click De-leverage**
   - [ ] Button to restore 20% margin safety buffer
   - [ ] Preview which positions sell
   - [ ] Confirmation with slippage estimate
   - [ ] Execute via broker API

4. **Audit Log Integration**
   - [ ] Log every margin-check event
   - [ ] Log de-leverage actions
   - [ ] Compliance reporting
   - [ ] Historical margin events

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `LiquidationEditor.test.jsx` | Ghost order display, de-leverage action |
| `GhostOrder.test.jsx` | Order preview, slippage calculation |

### Test Coverage Target: **90%**

---

## Route Integration

**Route:** `/guardian/margin`

**Macro Task:** The Guardian

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

