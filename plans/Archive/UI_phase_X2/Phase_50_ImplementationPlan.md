# Phase 50: Fixed Income & Yield Curve Visualization

> **Phase ID**: 50 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Monitors the baseline cost of money (the 'Climate' of the Yellowstone ecosystem) to protect capital preservation layers.

---

## Overview

Comprehensive UI for managing bond ladders and analyzing the sovereign yield curve.

---

## Sub-Deliverable 50.1: Bond Ladder Construction Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/FixedIncome/BondLadder.jsx` | Drag-and-drop ladder |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/BondLadder.css` | Styling |
| `[NEW]` | `frontend2/src/stores/fixedIncomeStore.js` | Bond state management |
| `[NEW]` | `services/analysis/fixed_income_service.py` | WAL calculation |
| `[NEW]` | `web/api/fixed_income_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Draggable D3 Bars**
   - [ ] Real-time update to `useFixedIncomeStore` (< 100ms)
   - [ ] Visual maturity timeline (1-30 years)
   - [ ] Click to add/remove bonds

2. **Weighted Average Life (WAL)**
   - [ ] Auto-calculate based on constituent par values
   - [ ] Display in header widget
   - [ ] Update on any bar change

3. **Liquidity Gap Indicators**
   - [ ] Red 'Starvation' pulse for years with zero maturities
   - [ ] High-contrast accessibility
   - [ ] Tooltip showing gap impact

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BondLadder.test.jsx` | Drag works, WAL updates, gap indicators |
| `fixedIncomeStore.test.js` | State updates < 100ms |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_fixed_income_service.py` | `test_wal_calculation`, `test_liquidity_gap_detection` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 50.2: Real-time Yield Curve (FRED API) Plotter

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/FixedIncome/YieldCurve.jsx` | Interactive plotter |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/YieldCurve.css` | Styling |
| `[NEW]` | `services/data/fred_service.py` | FRED API integration |

### Verbose Acceptance Criteria

1. **FRED API Integration**
   - [ ] Kafka topic `macro-fred-updates` subscription
   - [ ] < 500ms lag monitoring
   - [ ] Fallback to cached data on API failure

2. **Curve Animation**
   - [ ] Framer Motion shift animation over 12-month history
   - [ ] Slider to scrub through time
   - [ ] Current vs historical overlay

3. **Recession Signal**
   - [ ] Auto-alert when 10Y-2Y spread < 0bps
   - [ ] Visual inversion warning
   - [ ] Historical inversion markers

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `YieldCurve.test.jsx` | Curve renders, animation, inversion alert |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/data/test_fred_service.py` | `test_fred_api_fetch`, `test_inversion_detection`, `test_kafka_lag_monitoring` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 50.3: Duration & Convexity Risk Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/FixedIncome/DurationGauges.jsx` | Risk gauges |
| `[NEW]` | `frontend2/src/widgets/FixedIncome/DurationGauges.css` | Styling |

### Verbose Acceptance Criteria

1. **Rate Shock Sensitivity**
   - [ ] +/- 100bps shock calculation (Taylor Series)
   - [ ] Display dollar impact on portfolio
   - [ ] Percentage change visualization

2. **Convexity Warning**
   - [ ] Visual 'Stress Zone' for negative convexity
   - [ ] Impact on price-yield relationship
   - [ ] Tooltip explanation

3. **Data Verification**
   - [ ] Source from Postgres time-series tables
   - [ ] Auditability trail
   - [ ] Last updated timestamp

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DurationGauges.test.jsx` | Gauges render, shock calculation, stress zone |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_fixed_income_service.py` | `test_duration_calculation`, `test_convexity_calculation`, `test_rate_shock_impact` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/analytics/fixed-income`

**Macro Task:** Climate Monitoring

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=FixedIncome

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_fixed_income_service.py tests/data/test_fred_service.py -v --cov=services
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/analytics/fixed-income
# Verify: Bond ladder drag works, yield curve animates, gauges update
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 50 detailed implementation plan |
