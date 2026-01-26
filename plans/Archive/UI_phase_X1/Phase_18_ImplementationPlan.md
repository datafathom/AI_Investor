# Phase 18: Philanthropy & Impact Investing Dashboard

> **Phase 61** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Completes the homeostasis loop by routing 'Excess Alpha' back to the external environment.

---

## Overview

Manages automated charitable routing and ESG impact tracking for responsible wealth management.

---

## Sub-Deliverable 61.1: Excess Alpha Donation Routing Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Philanthropy/DonationRouter.jsx` | Router widget |
| `[NEW]` | `frontend2/src/widgets/Philanthropy/DonationRouter.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Philanthropy/CharitySelector.jsx` | Charity picker |
| `[NEW]` | `frontend2/src/services/philanthropyService.js` | Charity API |

### Verbose Acceptance Criteria

1. **GivingBlock/CharityNavigator Integration**
   - [ ] API integration for charity lookup
   - [ ] Charity ratings and reviews display
   - [ ] Secure fund routing through verified channels
   - [ ] Tax receipt automation

2. **Tax-Deduction Alpha Tracking**
   - [ ] Real-time tracking of tax savings from donations
   - [ ] "Donation Alpha": Marginal tax rate × donation
   - [ ] YTD donation summary
   - [ ] Projected tax impact

3. **Impact Pulse Visualization**
   - [ ] Show real-world projects funded
   - [ ] Progress bars for funded projects
   - [ ] Impact metrics: meals served, trees planted, etc.
   - [ ] "Your Impact Story" narrative generation

4. **Threshold Configuration**
   - [ ] Define "Enough" threshold
   - [ ] Auto-donate profits above threshold
   - [ ] Monthly, quarterly, or annual donation cycles
   - [ ] Allocation across multiple charities

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/philanthropy/charities` | GET | Charity search |
| `/api/v1/philanthropy/donate` | POST | Execute donation |
| `/api/v1/philanthropy/impact` | GET | Impact metrics |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DonationRouter.test.jsx` | Routing works, charity selection |
| `CharitySelector.test.jsx` | Search works, ratings display |
| `philanthropyService.test.js` | API integration, donation flow |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 61.2: ESG Score Aggregator

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Philanthropy/ESGGauges.jsx` | ESG gauges |
| `[NEW]` | `frontend2/src/widgets/Philanthropy/ESGGauges.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Philanthropy/SinStockAlert.jsx` | Sin stock warning |

### Verbose Acceptance Criteria

1. **E, S, G Component Gauges**
   - [ ] Circular gauge for Environmental score (0-100)
   - [ ] Circular gauge for Social score (0-100)
   - [ ] Circular gauge for Governance score (0-100)
   - [ ] Update via Kafka macro feeds

2. **Sin Stock Filter**
   - [ ] User-defined "sin stock" categories
   - [ ] Default: Tobacco, Arms, Gambling
   - [ ] Auto-alert on portfolio exposure
   - [ ] "Sell" quick action button

3. **Portfolio Karma Score**
   - [ ] Aggregated ESG score in header
   - [ ] Weighted by position size
   - [ ] Trend over time (improving/declining)
   - [ ] Comparison to benchmark

4. **Data Sources**
   - [ ] MSCI ESG ratings
   - [ ] Sustainalytics scores
   - [ ] Carbon disclosure project data
   - [ ] Data freshness indicator

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ESGGauges.test.jsx` | All three gauges render, scores update |
| `SinStockAlert.test.jsx` | Alert appears, sell action works |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 61.3: Carbon Footprint vs Portfolio Return Scatterplot

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Philanthropy/CarbonFootprint.jsx` | Chart widget |
| `[NEW]` | `frontend2/src/widgets/Philanthropy/CarbonFootprint.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Philanthropy/CarbonOffset.jsx` | Offset action |

### Verbose Acceptance Criteria

1. **D3.js Scatterplot**
   - [ ] X-axis: Carbon intensity (tons CO2 / $M revenue)
   - [ ] Y-axis: Returns (%)
   - [ ] Each point = one holding
   - [ ] Size = position weight

2. **Regression Line**
   - [ ] Calculate correlation between returns and carbon
   - [ ] Display regression line
   - [ ] R² value and p-value
   - [ ] Confidence bands

3. **One-Click Carbon Offset**
   - [ ] Calculate portfolio carbon footprint
   - [ ] Suggest offset amount (tons)
   - [ ] Integration with carbon credit marketplaces
   - [ ] Certificate of offset

4. **Emissions Breakdown**
   - [ ] Hover shows company's Scope 1/2/3 emissions
   - [ ] Compare to industry average
   - [ ] Trend over time
   - [ ] Decarbonization targets

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CarbonFootprint.test.jsx` | Scatter renders, regression line |
| `CarbonOffset.test.jsx` | Offset calculation, purchase flow |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/impact`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

