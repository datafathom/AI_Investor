# Phase 9: Tax-Advantaged Strategy & Harvesting UI

> **Phase 52** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Ensures the recycling of 'Dead Capital' through loss harvesting to fuel new growth.

---

## Overview

Automated tools for identification and execution of tax-alpha opportunities. Tax efficiency can add 0.5-1% annually to returns, making this a critical component of total wealth management.

---

## Sub-Deliverable 52.1: Unrealized Loss Identification Grid (Wash-Sale Protected)

### Description
Filterable grid of loss positions eligible for harvesting, with automatic wash-sale violation prevention.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Tax/LossHarvestGrid.jsx` | Main grid widget |
| `[NEW]` | `frontend2/src/widgets/Tax/LossHarvestGrid.css` | Grid styling |
| `[NEW]` | `frontend2/src/widgets/Tax/WashSaleWarning.jsx` | Warning component |
| `[NEW]` | `frontend2/src/services/taxService.js` | Tax calculation service |
| `[NEW]` | `frontend2/src/stores/taxStore.js` | Zustand tax store |

### Verbose Acceptance Criteria

1. **Postgres 30-Day History Query**
   - [ ] Query buy-side history for each position in last 30 days
   - [ ] Prevent harvesting if wash-sale violation would occur
   - [ ] "Wash-Sale Risk" badge on ineligible positions
   - [ ] Countdown timer: "Eligible in X days"

2. **Tax Savings Alpha Calculation**
   - [ ] Calculate potential tax savings per position
   - [ ] Formula: `Loss × Marginal Tax Rate`
   - [ ] Display as dollar amount: "Tax Alpha: $1,234"
   - [ ] Sort by highest tax-alpha opportunity

3. **One-Click Harvest & Replace**
   - [ ] Suggest correlated but non-identical replacement assets
   - [ ] Correlation threshold: >0.8 correlation, not substantially identical
   - [ ] Example: Sell SPY, buy IVV or VOO
   - [ ] Confirmation modal with tax impact summary

4. **Grid Features**
   - [ ] Columns: Ticker, Unrealized Loss, Days Held, Wash-Sale Status, Tax Alpha
   - [ ] Sortable by any column
   - [ ] Filter by: Eligible only, Amount threshold, Asset class
   - [ ] Bulk selection for batch harvesting

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/tax/harvesting-candidates` | GET | Positions eligible for harvesting |
| `/api/v1/tax/wash-sale-check` | POST | Check if transaction would trigger wash-sale |
| `/api/v1/tax/replacement-suggestions` | GET | Correlated replacement assets |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `LossHarvestGrid.test.jsx` | Grid renders, sort works, filter applies, wash-sale badge shows |
| `WashSaleWarning.test.jsx` | Warning displays, countdown accurate |
| `taxService.test.js` | Tax alpha calculation, wash-sale detection |
| `taxStore.test.js` | State updates correctly |

### Test Coverage Target: **90%** (tax-critical)

---

## Sub-Deliverable 52.2: Automated Tax-Loss Harvesting Toggle

### Description
Global switch to allow autonomous agents to execute harvesting trades with appropriate safeguards.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Tax/HarvestingToggle.jsx` | Toggle widget |
| `[NEW]` | `frontend2/src/widgets/Tax/HarvestingToggle.css` | Toggle styling |
| `[MODIFY]` | `frontend2/src/components/Taskbar/TaskbarIcon.jsx` | Add Shield icon |

### Verbose Acceptance Criteria

1. **OAuth 2.0 Biometric Confirmation**
   - [ ] Secondary authentication required for activation
   - [ ] Support FaceID, TouchID, Windows Hello
   - [ ] Fallback to 6-digit PIN
   - [ ] Session expiry: 24 hours

2. **Visual Shield Indicator**
   - [ ] "Shield" icon appears in Taskbar during active harvesting
   - [ ] Icon pulses when harvest executed
   - [ ] Tooltip shows: "Auto-Harvesting Active - X positions monitored"
   - [ ] Click to view recent harvesting activity

3. **ProtectorAgent Integration**
   - [ ] Integrate with `ProtectorAgent` for sector exposure limits
   - [ ] Prevent harvesting that would breach concentration limits
   - [ ] Coordination with other autonomous agents
   - [ ] Activity logged to `UnifiedActivityService`

4. **Configuration Options**
   - [ ] Minimum loss threshold to trigger ($500 default)
   - [ ] Maximum daily harvesting budget
   - [ ] Excluded positions (manual override)
   - [ ] Schedule: Market hours only vs 24/7

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `HarvestingToggle.test.jsx` | Toggle state, biometric flow mock, shield icon appears |

### Test Coverage Target: **90%**

---

## Sub-Deliverable 52.3: Long-term vs. Short-term Capital Gains Forecaster

### Description
Timeline visualizer showing when positions transition to long-term status, enabling optimal tax planning.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Tax/GainsForecaster.jsx` | Forecaster widget |
| `[NEW]` | `frontend2/src/widgets/Tax/GainsForecaster.css` | Widget styling |
| `[NEW]` | `frontend2/src/widgets/Tax/CountdownIndicator.jsx` | Individual countdown |

### Verbose Acceptance Criteria

1. **Framer Motion Countdown Indicators**
   - [ ] Animated countdown for positions within 30 days of LTCG status
   - [ ] Visual urgency: Green (>30 days), Yellow (7-30 days), Red (<7 days)
   - [ ] "🎉 LTCG!" celebration animation when threshold crossed
   - [ ] Sort by "Time to LTCG"

2. **Tax Liability Projections**
   - [ ] Three scenario comparison:
     - Hold All: Tax if sold after LTCG
     - Sell All Now: Tax at STCG rates
     - Partial Harvest: Optimal tax-loss harvesting scenario
   - [ ] Visual bar chart comparing scenarios
   - [ ] Net difference calculation

3. **Exportable CSV**
   - [ ] "Export for CPA" button
   - [ ] Columns: Ticker, Acquisition Date, Cost Basis, Current Value, Gain/Loss, LTCG Date
   - [ ] Formatted for TurboTax/TaxAct import
   - [ ] Include summary row with totals

4. **Timeline View**
   - [ ] Horizontal timeline showing LTCG eligibility dates
   - [ ] Cluster positions by eligibility month
   - [ ] Hover to see position details
   - [ ] "Mark as Held" for commitment tracking

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `GainsForecaster.test.jsx` | Timeline renders, countdown correct, scenarios calculate |
| `CountdownIndicator.test.jsx` | Animation triggers, color changes at thresholds |

### Test Coverage Target: **85%**

---

## Widget Registry Entries

```javascript
{
  id: 'loss-harvest-grid',
  name: 'Tax-Loss Harvesting',
  component: lazy(() => import('../../widgets/Tax/LossHarvestGrid')),
  category: 'Tax',
  defaultSize: { width: 600, height: 450 }
},
{
  id: 'harvesting-toggle',
  name: 'Auto-Harvest Toggle',
  component: lazy(() => import('../../widgets/Tax/HarvestingToggle')),
  category: 'Tax',
  defaultSize: { width: 300, height: 200 }
},
{
  id: 'gains-forecaster',
  name: 'Capital Gains Forecaster',
  component: lazy(() => import('../../widgets/Tax/GainsForecaster')),
  category: 'Tax',
  defaultSize: { width: 550, height: 400 }
}
```

---

## Route Integration

**Route:** `/strategist/tax`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

