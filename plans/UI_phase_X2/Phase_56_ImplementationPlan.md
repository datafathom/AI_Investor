# Phase 56: Multi-Currency Cash Management & FX Conversion

> **Phase ID**: 56 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Manages the 'Pulse' of global liquidity and jurisdictional arbitrage.

---

## Overview

Real-time dashboard for managing multi-currency balances and FX hedging.

---

## Sub-Deliverable 56.1: Global Cash Balance 'Pulse' Widget

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Cash/CashPulse.jsx` | Multi-currency viewer |
| `[NEW]` | `frontend2/src/widgets/Cash/CashPulse.css` | Styling |
| `[NEW]` | `frontend2/src/stores/cashStore.js` | Cash state management |
| `[NEW]` | `services/trading/fx_service.py` | FX rate service |
| `[NEW]` | `web/api/cash_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Real-time FX Rates**
   - [ ] Kafka topic `fx-stream-global` updates every 10s
   - [ ] Support USD, EUR, GBP, JPY, CHF, CAD
   - [ ] Rate change indicators (+/-)

2. **Heat Indicators**
   - [ ] Visual 'Heat' for high overnight interest rates
   - [ ] USD vs JPY spread display
   - [ ] Carry trade opportunity alerts

3. **Base Currency Toggle**
   - [ ] Zustand state mapping for instant conversion
   - [ ] One-click base currency switch
   - [ ] Total valuation in selected base

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CashPulse.test.jsx` | Rates display, heat indicators, toggle works |
| `cashStore.test.js` | Currency conversion, state updates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/trading/test_fx_service.py` | `test_rate_fetch`, `test_carry_trade_detection`, `test_kafka_stream` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 56.2: Limit-Order FX Conversion Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Cash/FXConverter.jsx` | Order entry |
| `[NEW]` | `frontend2/src/widgets/Cash/FXConverter.css` | Styling |

### Verbose Acceptance Criteria

1. **Iceberg Orders**
   - [ ] Support iceberg orders for large swaps
   - [ ] Minimize market impact
   - [ ] Configurable slice size

2. **Bid/Ask Spread Gauge**
   - [ ] Visual gauge with 10bps precision
   - [ ] Real-time Kafka feed
   - [ ] Historical spread comparison

3. **Risk Guardrails**
   - [ ] Integration with `RiskGuardrailService`
   - [ ] Prevent > 15% currency exposure
   - [ ] Confirmation for large orders

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `FXConverter.test.jsx` | Order entry works, spread displays, guardrail triggers |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/trading/test_fx_service.py` | `test_iceberg_order`, `test_exposure_limit`, `test_order_execution` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 56.3: Interest-Bearing Cash Optimization Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Cash/CashOptimizer.jsx` | Sweep suggestions |
| `[NEW]` | `frontend2/src/widgets/Cash/CashOptimizer.css` | Styling |

### Verbose Acceptance Criteria

1. **Sweep Suggestions**
   - [ ] Auto-suggest when idle cash > $50,000
   - [ ] MMF/T-Bill recommendations
   - [ ] One-click sweep execution

2. **Overnight Repo Comparison**
   - [ ] Table: US, EU, UK repo rates
   - [ ] Best rate highlight
   - [ ] Historical yield tracking

3. **Visualizations**
   - [ ] D3.js area charts
   - [ ] 20px backdrop-blur containers
   - [ ] Yield projection over time

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CashOptimizer.test.jsx` | Suggestions display, comparison table, charts render |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/trading/test_fx_service.py` | `test_sweep_logic`, `test_repo_rate_fetch`, `test_yield_calculation` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/cash`

**Macro Task:** Global Liquidity Pulse

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Cash

# Backend
.\venv\Scripts\python.exe -m pytest tests/trading/test_fx_service.py -v --cov=services/trading
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/strategist/cash
# Verify: Pulse updates, FX converter works, optimizer suggests sweeps
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 56 detailed implementation plan |
