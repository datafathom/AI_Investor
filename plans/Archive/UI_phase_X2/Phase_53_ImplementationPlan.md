# Phase 53: Global Macro & Commodities Heatmaps

> **Phase ID**: 53 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Monitors the 'Environmental Conditions' (Supply Chains, Politics) that precede price oscillations.

---

## Overview

Mapping of global trade, political alpha, and commodity term structures.

---

## Sub-Deliverable 53.1: Interactive D3 World Map (Shipping & Politics)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Macro/WorldMap.jsx` | Choropleth map |
| `[NEW]` | `frontend2/src/widgets/Macro/WorldMap.css` | Styling |
| `[NEW]` | `frontend2/src/stores/macroStore.js` | Macro state management |
| `[NEW]` | `services/analysis/macro_service.py` | Macro data aggregation |
| `[NEW]` | `web/api/macro_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Political Insider Nodes**
   - [ ] Display `POLITICAL_INSIDER` nodes from Neo4j
   - [ ] 13F filing locations and trade volumes
   - [ ] Nancy Pelosi Index overlay

2. **Shipping Congestion**
   - [ ] Real-time icons from Marine Traffic API via Kafka
   - [ ] Port delay indicators
   - [ ] Supply chain bottleneck alerts

3. **Regional CPI/PPI**
   - [ ] Click region to update `useMacroStore`
   - [ ] Display localized inflation metrics
   - [ ] Historical trend overlay

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `WorldMap.test.jsx` | Map renders, region click, shipping icons |
| `macroStore.test.js` | State updates on region select |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_macro_service.py` | `test_political_node_fetch`, `test_shipping_data_integration`, `test_cpi_ppi_fetch` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 53.2: Futures Curve Contango/Backwardation Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Macro/FuturesCurve.jsx` | D3.js curve plotter |
| `[NEW]` | `frontend2/src/widgets/Macro/FuturesCurve.css` | Styling |
| `[NEW]` | `services/market/futures_service.py` | Futures data |

### Verbose Acceptance Criteria

1. **Roll Yield Markers**
   - [ ] Visual opportunity markers on curve
   - [ ] Automated yield calculation
   - [ ] Contango/backwardation labels

2. **Cross-Commodity Spreads**
   - [ ] Crack Spread (Oil/Gas) chart
   - [ ] 60 FPS Canvas rendering
   - [ ] Spread calculator tool

3. **Real-time Updates**
   - [ ] Kafka event stream (< 200ms latency)
   - [ ] Price tick animation
   - [ ] Last update timestamp

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `FuturesCurve.test.jsx` | Curve renders, roll markers, spread calc |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/market/test_futures_service.py` | `test_contango_detection`, `test_roll_yield_calculation`, `test_spread_calculation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 53.3: Inflation-Sensitive Asset Correlation Matrix (Neo4j)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Macro/InflationMatrix.jsx` | Graph visualization |
| `[NEW]` | `frontend2/src/widgets/Macro/InflationMatrix.css` | Styling |

### Verbose Acceptance Criteria

1. **Neo4j Edge Mapping**
   - [ ] `INFLATION_HEDGE` edges for positive correlation
   - [ ] `DEFLATION_VICTIM` edges for negative correlation
   - [ ] Cypher query execution < 150ms

2. **Dynamic Clustering**
   - [ ] Cluster by sensitivity (beta) to 10Y break-even
   - [ ] Visual node grouping
   - [ ] Drag to explore

3. **Responsiveness**
   - [ ] Graph updates maintain UI responsiveness
   - [ ] Lazy loading for large graphs
   - [ ] Search/filter nodes

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `InflationMatrix.test.jsx` | Graph renders, clustering works, search |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_macro_service.py` | `test_inflation_hedge_query`, `test_cypher_performance`, `test_beta_sensitivity_calculation` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/observer/macro`

**Macro Task:** Environmental Foresight

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Macro

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_macro_service.py tests/market/test_futures_service.py -v --cov=services
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/observer/macro
# Verify: World map interactive, futures curve updates, matrix clusters
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 53 detailed implementation plan |
