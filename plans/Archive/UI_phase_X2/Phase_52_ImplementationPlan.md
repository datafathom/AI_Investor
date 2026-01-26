# Phase 52: Tax-Advantaged Strategy & Harvesting UI

> **Phase ID**: 52 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Ensures the recycling of 'Dead Capital' through loss harvesting to fuel new growth.

---

## Overview

Automated tools for identification and execution of tax-alpha opportunities.

---

## Sub-Deliverable 52.1: Unrealized Loss Identification Grid (Wash-Sale Protected)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Tax/LossHarvestGrid.jsx` | Filterable grid |
| `[NEW]` | `frontend2/src/widgets/Tax/LossHarvestGrid.css` | Styling |
| `[NEW]` | `frontend2/src/stores/taxStore.js` | Tax state management |
| `[NEW]` | `services/tax/harvest_service.py` | Wash-sale logic |
| `[NEW]` | `web/api/tax_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Wash-Sale Protection**
   - [ ] Query Postgres for 30-day buy-side history
   - [ ] Flag positions that would trigger wash-sale
   - [ ] Warning icon with explanation

2. **Tax Savings Alpha**
   - [ ] Real-time calculation per position
   - [ ] Based on marginal tax rate presets (22%, 32%, 37%)
   - [ ] Sort by savings potential

3. **Harvest & Replace Logic**
   - [ ] One-click suggestion of correlated assets
   - [ ] Neo4j correlation graph query
   - [ ] Avoid identical assets (wash-sale)

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `LossHarvestGrid.test.jsx` | Grid renders, wash-sale warning, replace suggestions |
| `taxStore.test.js` | Tax rate presets, savings calculation |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/tax/test_harvest_service.py` | `test_wash_sale_detection`, `test_tax_savings_calculation`, `test_correlated_asset_suggestion` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 52.2: Automated Tax-Loss Harvesting Toggle

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Tax/HarvestToggle.jsx` | Global switch |
| `[NEW]` | `frontend2/src/widgets/Tax/HarvestToggle.css` | Styling |

### Verbose Acceptance Criteria

1. **Biometric Confirmation**
   - [ ] Secondary OAuth 2.0 biometric for activation
   - [ ] Cool-down period after deactivation
   - [ ] Audit log entry

2. **Visual Feedback**
   - [ ] 'Shield' icon in Taskbar (70% opacity)
   - [ ] Active harvesting indicator
   - [ ] Trade count display

3. **ProtectorAgent Integration**
   - [ ] Sector exposure limits enforcement
   - [ ] Position size limits
   - [ ] Auto-pause on limit breach

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `HarvestToggle.test.jsx` | Toggle state, biometric mock, shield icon |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/tax/test_harvest_service.py` | `test_automated_harvest_execution`, `test_sector_limit_enforcement` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 52.3: Long-term vs. Short-term Capital Gains Forecaster

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Tax/GainsForecaster.jsx` | Timeline visualizer |
| `[NEW]` | `frontend2/src/widgets/Tax/GainsForecaster.css` | Styling |

### Verbose Acceptance Criteria

1. **Countdown Indicators**
   - [ ] Framer Motion countdown for assets within 30 days of LT status
   - [ ] Visual calendar view
   - [ ] Notification opt-in

2. **Tax Liability Projection**
   - [ ] Three scenarios: Hold, Sell All, Partial Harvest
   - [ ] D3.js area charts comparison
   - [ ] Side-by-side view

3. **CPA Export**
   - [ ] CSV formatted for CPA ingestion
   - [ ] SHA-256 integrity hash
   - [ ] IRS-compliant format

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `GainsForecaster.test.jsx` | Countdown renders, scenarios compare, CSV export |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/tax/test_harvest_service.py` | `test_lt_st_classification`, `test_scenario_projection`, `test_csv_export_format` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/tax`

**Macro Task:** Dead Capital Recycling

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Tax

# Backend
.\venv\Scripts\python.exe -m pytest tests/tax/ -v --cov=services/tax
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/strategist/tax
# Verify: Grid shows losses, toggle requires auth, forecaster displays scenarios
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 52 detailed implementation plan |
