# Phase 67: Real-Estate & Illiquid Asset Tracking

> **Phase ID**: 67 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Incorporates 'Slow Capital' into the high-frequency Net Worth model for total wealth homeostasis.

---

## Overview

Tracking of physical assets, private equity, and manual entries.

---

## Sub-Deliverable 67.1: Manual Asset Entry (Physical Property, Art, Private Equity)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/ManualEntry.jsx` | Entry forms |
| `[NEW]` | `frontend2/src/widgets/Assets/ManualEntry.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Assets/AssetCategories.jsx` | Category picker |
| `[NEW]` | `frontend2/src/stores/wealthStore.js` | Wealth state |
| `[NEW]` | `services/portfolio/assets_service.py` | Asset persistence |
| `[NEW]` | `web/api/assets_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Neo4j Entity Linking**
   - [ ] Link to `ENTITY` nodes for jurisdictional mapping
   - [ ] Tax implications per entity type
   - [ ] Ownership percentage tracking

2. **Document Upload**
   - [ ] Appraisals and insurance uploads
   - [ ] Vault integration with "Missing Document" warnings
   - [ ] Expiration tracking

3. **TotalWealth Merge**
   - [ ] Single Zustand slice for liquid + illiquid
   - [ ] Combined Net Worth calculation
   - [ ] View toggle: Liquid/Illiquid/All

4. **Category Support**
   - [ ] Real Estate (Primary, Rental, Vacation)
   - [ ] Art & Collectibles
   - [ ] Private Equity/Venture
   - [ ] Vehicles & Personal Property

### Test Coverage Target: **80%**

---

## Sub-Deliverable 67.2: Estimated Valuation Depreciation/Appreciation Slider

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/ValuationSlider.jsx` | Value adjuster |
| `[NEW]` | `frontend2/src/widgets/Assets/ValuationSlider.css` | Styling |

### Verbose Acceptance Criteria

1. **Real-time Impact**
   - [ ] D3.js gauges update as slider moves
   - [ ] Delta display: "+$50,000 (↑2.1%)"
   - [ ] Save/Undo functionality

2. **API Integration**
   - [ ] Zillow/Redfin property estimates
   - [ ] "Zestimate" comparison
   - [ ] Auto-update toggle

3. **Historical Timeline**
   - [ ] TimescaleDB storage
   - [ ] Value chart over time
   - [ ] Inflation comparison

### Test Coverage Target: **80%**

---

## Sub-Deliverable 67.3: Unified Wealth 'Net Worth' Circular Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/NetWorthGauges.jsx` | D3.js visualization |
| `[NEW]` | `frontend2/src/widgets/Assets/NetWorthGauges.css` | Styling |

### Verbose Acceptance Criteria

1. **Dual-Ring Design**
   - [ ] Inner ring: Liquid (Stocks/Crypto/Cash)
   - [ ] Outer ring: Illiquid (Real Estate/PE/Art)
   - [ ] Color-coded segments

2. **Center Display**
   - [ ] Total Net Worth prominently shown
   - [ ] 24h change with delta
   - [ ] "All-Time High" badge

3. **Framer Motion Animation**
   - [ ] 60 FPS ring animation on load
   - [ ] Smooth segment transitions
   - [ ] Hover expansion for details

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/assets`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 67 |
