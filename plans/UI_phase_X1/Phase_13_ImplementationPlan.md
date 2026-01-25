# Phase 13: Multi-Currency Cash Management & FX Conversion

> **Phase 56** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Manages the 'Pulse' of global liquidity and jurisdictional arbitrage.

---

## Overview

Real-time dashboard for managing multi-currency balances and FX hedging across global markets.

---

## Sub-Deliverable 56.1: Global Cash Balance 'Pulse' Widget

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Currency/CashPulse.jsx` | Main widget |
| `[NEW]` | `frontend2/src/widgets/Currency/CashPulse.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Currency/CurrencyCard.jsx` | Per-currency card |
| `[NEW]` | `frontend2/src/stores/currencyStore.js` | Zustand store |

### Verbose Acceptance Criteria

1. **Kafka FX Rate Updates**
   - [ ] Subscribe to `fx-stream-global` topic
   - [ ] Update rates every 10 seconds
   - [ ] Fallback to REST if Kafka unavailable
   - [ ] "Stale Data" warning if >1 minute old

2. **Heat Indicators for Interest Rates**
   - [ ] Visual "Heat" color for currencies with high overnight rates
   - [ ] Gradient: Cool (low rates) → Hot (high rates)
   - [ ] Tooltip shows current overnight rate
   - [ ] Compare to USD base rate

3. **Base Currency Toggle**
   - [ ] One-click toggle using Zustand state
   - [ ] Options: USD, EUR, GBP, JPY, CHF
   - [ ] All values recalculate instantly
   - [ ] "Default" option persisted to user profile

4. **Aggregated Display**
   - [ ] Total cash across all currencies in base currency
   - [ ] Pie chart of currency allocation
   - [ ] 24h change with color indicator
   - [ ] "Idle Cash" alert when significant uninvested amounts

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/currency/balances` | GET | Cash balances by currency |
| `/ws/fx-stream` | WS | Real-time FX rates |
| `/api/v1/currency/overnight-rates` | GET | Interest rates by currency |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CashPulse.test.jsx` | Renders currencies, rate updates, base currency toggle |
| `CurrencyCard.test.jsx` | Heat indicator, balance display |
| `currencyStore.test.js` | Rate updates, base currency change |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 56.2: Limit-Order FX Conversion Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Currency/FXConversion.jsx` | Conversion widget |
| `[NEW]` | `frontend2/src/widgets/Currency/FXConversion.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Currency/IcebergOrder.jsx` | Iceberg builder |

### Verbose Acceptance Criteria

1. **Iceberg Order Support**
   - [ ] Build iceberg orders to minimize market impact
   - [ ] Configure visible vs hidden quantity
   - [ ] Execution report showing fills over time
   - [ ] Cancel remaining functionality

2. **Bid/Ask Spread Gauge**
   - [ ] Visual gauge with 10bps precision
   - [ ] Historical spread comparison
   - [ ] "Wide Spread Warning" when >20bps
   - [ ] Best execution timing suggestions

3. **RiskGuardrailService Integration**
   - [ ] Prevent unauthorized currency exposure
   - [ ] Max currency concentration limits
   - [ ] Pre-trade check before order submission
   - [ ] Warning modal for limit breaches

4. **Order Entry**
   - [ ] From/To currency selection
   - [ ] Amount input with validation
   - [ ] Rate limit order price
   - [ ] GTD/GTC order duration options

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `FXConversion.test.jsx` | Order entry, validation, spread display |
| `IcebergOrder.test.jsx` | Visible/hidden quantity, cancel button |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 56.3: Interest-Bearing Cash Optimization Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Currency/CashOptimizer.jsx` | Optimizer widget |
| `[NEW]` | `frontend2/src/widgets/Currency/CashOptimizer.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Currency/SweepSuggestion.jsx` | Sweep recommendation |

### Verbose Acceptance Criteria

1. **Automated Sweep Suggestions**
   - [ ] Alert when idle cash exceeds $50,000 threshold
   - [ ] Suggest optimal deployment: MMFs, T-Bills, Repos
   - [ ] One-click "Sweep" button to execute
   - [ ] Configurable threshold per user

2. **Overnight Repo Rate Comparison**
   - [ ] Table comparing US, EU, UK repo rates
   - [ ] Historical trend sparklines
   - [ ] "Best Yield" indicator
   - [ ] Net yield after FX conversion costs

3. **Historical Yield Tracking**
   - [ ] D3.js area charts for yield over time
   - [ ] Compare actual yield to benchmark
   - [ ] Calculate total interest earned YTD
   - [ ] Export for tax reporting

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CashOptimizer.test.jsx` | Suggestions render, threshold works, sweep action |
| `SweepSuggestion.test.jsx` | Recommendation display, click handler |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/currency`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

