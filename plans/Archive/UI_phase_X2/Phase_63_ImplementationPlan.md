# Phase 63: Corporate Actions & Earnings Integrated GUI

> **Phase ID**: 63 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Tracks the fundamental 'Life Cycles' of constituents within the Yellowstone ecosystem.

---

## Overview

Interactive management of dividends, splits, and earnings cycles.

---

## Sub-Deliverable 63.1: Interactive Earnings Calendar with 'Whisper Number' Integration

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCalendar.jsx` | Calendar view |
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCalendar.css` | Styling |
| `[NEW]` | `frontend2/src/stores/corporateStore.js` | Corporate events state |
| `[NEW]` | `services/market/earnings_service.py` | Earnings data |
| `[NEW]` | `web/api/corporate_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Implied Move Indicator**
   - [ ] Derived from current options straddle pricing
   - [ ] Visual bar showing expected range
   - [ ] Historical accuracy comparison

2. **Debate Chamber Link**
   - [ ] One-click to discuss upcoming earnings with Bull/Bear personas
   - [ ] Pre-populated context from company data
   - [ ] Trade recommendation output

3. **Portfolio Significance Filter**
   - [ ] Filter by beta-weighted exposure
   - [ ] Sector concentration impact
   - [ ] High-impact events highlighted

### Test Coverage Target: **80%**

---

## Sub-Deliverable 63.2: Dividend Reinvestment (DRIP) Management Console

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/DRIPConsole.jsx` | DRIP controls |
| `[NEW]` | `frontend2/src/widgets/Corporate/DRIPConsole.css` | Styling |

### Verbose Acceptance Criteria

1. **Yield on Cost**
   - [ ] Calculate and display per dividend payer
   - [ ] D3.js sparkline history
   - [ ] Compare to current yield

2. **Dividend Snowball**
   - [ ] 5-year projection via area charts
   - [ ] Compound growth visualization
   - [ ] "What-if" DRIP toggle comparison

3. **Income vs Expenses**
   - [ ] Annual dividend income total
   - [ ] Compare to annual expenses ("Enough" metric)
   - [ ] Gap closure projection

### Test Coverage Target: **80%**

---

## Sub-Deliverable 63.3: Stock Split & Spin-off Adjustment Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/SplitSpinoff.jsx` | Event tracker |
| `[NEW]` | `frontend2/src/widgets/Corporate/SplitSpinoff.css` | Styling |

### Verbose Acceptance Criteria

1. **Cost Basis Adjustment**
   - [ ] Auto-display adjusted cost basis
   - [ ] TimescaleDB lookup for historical data
   - [ ] Tax lot tracking

2. **Event Notifications**
   - [ ] Taskbar stream for upcoming events
   - [ ] Ticker change alerts
   - [ ] Ex-date reminders

3. **Parent/Child Visualization**
   - [ ] Neo4j relationship edges
   - [ ] Visual company family tree
   - [ ] Click to view spin-off details

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/corporate`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 63 |
