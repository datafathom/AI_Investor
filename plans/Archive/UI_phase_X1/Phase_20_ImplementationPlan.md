# Phase 20: Corporate Actions & Earnings Integrated GUI

> **Phase 63** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Tracks the fundamental 'Life Cycles' of constituents within the Yellowstone ecosystem.

---

## Overview

Interactive management of dividends, splits, and earnings cycles with forward-looking intelligence.

---

## Sub-Deliverable 63.1: Interactive Earnings Calendar with 'Whisper Number' Integration

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCalendar.jsx` | Calendar widget |
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCalendar.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCard.jsx` | Per-company card |
| `[NEW]` | `frontend2/src/services/earningsService.js` | Earnings API |

### Verbose Acceptance Criteria

1. **Implied Move from Options**
   - [ ] Calculate expected move from straddle pricing
   - [ ] Display: "AAPL Implied Move: ±5.2%"
   - [ ] Historical accuracy comparison
   - [ ] "Overpriced" or "Underpriced" suggestion

2. **Debate Chamber Link**
   - [ ] One-click link to AI Debate Chamber
   - [ ] Pre-populate with earnings thesis
   - [ ] "Discuss AAPL Earnings" button
   - [ ] Historical debate outcomes

3. **Portfolio Significance Filter**
   - [ ] Filter by Beta-weighted exposure
   - [ ] "Material Impact" badge for high-weight positions
   - [ ] Sort by P&L impact potential
   - [ ] Exclude/include non-portfolio stocks

4. **Calendar Features**
   - [ ] Week/Month/Quarter view toggle
   - [ ] Before Market Open (BMO) vs After Market Close (AMC) indicator
   - [ ] Analyst consensus vs whisper number
   - [ ] Historical beat/miss track record

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/corporate/earnings` | GET | Earnings calendar |
| `/api/v1/corporate/whisper-numbers` | GET | Street whisper |
| `/api/v1/options/implied-move` | GET | Options-derived move |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EarningsCalendar.test.jsx` | Calendar renders, filter works |
| `EarningsCard.test.jsx` | Card display, implied move |
| `earningsService.test.js` | API integration |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 63.2: Dividend Reinvestment (DRIP) Management Console

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/DRIPConsole.jsx` | DRIP widget |
| `[NEW]` | `frontend2/src/widgets/Corporate/DRIPConsole.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Corporate/DividendSnowball.jsx` | Projection chart |

### Verbose Acceptance Criteria

1. **Per-Asset Toggle**
   - [ ] DRIP on/off toggle per holding
   - [ ] Bulk enable/disable actions
   - [ ] Save preferences to backend
   - [ ] Default setting for new purchases

2. **Yield on Cost Sparklines**
   - [ ] Calculate YoC for each dividend payer
   - [ ] Sparkline showing YoC trend
   - [ ] Compare to current yield
   - [ ] Highlight significant increases

3. **Dividend Snowball Projection**
   - [ ] 5-year projection visualization
   - [ ] Assumptions: current positions, reinvestment, growth rate
   - [ ] Multiple scenarios: Low/Med/High growth
   - [ ] "Time to Double" calculation

4. **Annual Income Summary**
   - [ ] Real-time projection of annual dividend income
   - [ ] Monthly breakdown chart
   - [ ] By sector/industry view
   - [ ] Tax-adjusted income

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DRIPConsole.test.jsx` | Toggles work, bulk actions |
| `DividendSnowball.test.jsx` | Projection chart renders |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 63.3: Stock Split & Spin-off Adjustment Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/CorporateActions.jsx` | Actions widget |
| `[NEW]` | `frontend2/src/widgets/Corporate/CorporateActions.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Corporate/SpinoffTree.jsx` | Parent/child graph |

### Verbose Acceptance Criteria

1. **Cost Basis Adjustment Display**
   - [ ] Automatic adjustment on split/spinoff
   - [ ] Before/after cost basis comparison
   - [ ] Per-share price adjustment
   - [ ] Total cost basis unchanged (for tax)

2. **Upcoming Actions Notifications**
   - [ ] Notification stream for upcoming events
   - [ ] Record date, ex-date, pay date display
   - [ ] Ticker change alerts (rebrand/spin-off)
   - [ ] "Action Required" badge if applicable

3. **Neo4j Parent/Child Visualization**
   - [ ] Graph view of spin-off relationships
   - [ ] Example: GE → GE Healthcare
   - [ ] Historical corporate tree
   - [ ] Click to navigate between entities

4. **Historical Actions Log**
   - [ ] Complete history of splits, dividends, spin-offs
   - [ ] Filter by action type
   - [ ] Export for tax records
   - [ ] Audit trail

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CorporateActions.test.jsx` | Actions list, notifications |
| `SpinoffTree.test.jsx` | Graph renders, navigation |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/corporate`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

