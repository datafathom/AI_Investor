# Phase 64: Advanced Margin & Collateral Management

> **Phase ID**: 64 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Prevents the 'Starvation' event of a margin call which leads to ecosystem collapse.

---

## Overview

Precision monitoring of buying power and liquidation risk.

---

## Sub-Deliverable 64.1: Maintenance Margin 'Danger Zone' Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/DangerZone.jsx` | Margin gauge |
| `[NEW]` | `frontend2/src/widgets/Margin/DangerZone.css` | Styling |
| `[NEW]` | `frontend2/src/stores/marginStore.js` | Margin state |
| `[NEW]` | `services/risk/margin_service.py` | Margin calculation |
| `[NEW]` | `web/api/margin_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Distance to Liquidate**
   - [ ] Calculate % buffer for top 5 leveraged positions
   - [ ] "The Gap" metric prominently displayed
   - [ ] Real-time Kafka price feed updates

2. **Visual Warning**
   - [ ] Red pulse when margin buffer < 15%
   - [ ] Progressive urgency coloring
   - [ ] Sound alert option

3. **useRiskStore Integration**
   - [ ] Real-time collateral revaluation
   - [ ] Cross-margin calculation
   - [ ] Position-level breakdown

### Test Coverage Target: **80%**

---

## Sub-Deliverable 64.2: Cross-Collateralization Asset Priority Toggle

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/AssetPriority.jsx` | Priority list |
| `[NEW]` | `frontend2/src/widgets/Margin/AssetPriority.css` | Styling |

### Verbose Acceptance Criteria

1. **Liquidation Hierarchy**
   - [ ] Drag-and-drop priority list
   - [ ] User defines which assets sold first
   - [ ] Visual priority numbers

2. **Impact Calculator**
   - [ ] Real-time margin impact of selling each asset
   - [ ] Cascade effect visualization
   - [ ] Optimal sequence suggestion

3. **Protected Assets**
   - [ ] Mark core holdings as "Protected"
   - [ ] Agents barred from touching
   - [ ] Visual shield icon

### Test Coverage Target: **80%**

---

## Sub-Deliverable 64.3: Automated Margin Call Liquidation Order Editor

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/GhostOrderViewer.jsx` | Broker preview |
| `[NEW]` | `frontend2/src/widgets/Margin/GhostOrderViewer.css` | Styling |

### Verbose Acceptance Criteria

1. **Worst Case Preview**
   - [ ] Visualize broker's auto-liquidation orders
   - [ ] Expected slippage calculation
   - [ ] Order book sweep simulation

2. **One-Click De-leverage**
   - [ ] Restore 20% margin safety buffer
   - [ ] Optimal position sizing
   - [ ] Confirmation with impact summary

3. **Audit Logging**
   - [ ] Every margin-check event logged
   - [ ] Risk governor trigger history
   - [ ] Regulatory compliance trail

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/guardian/margin`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 64 |
