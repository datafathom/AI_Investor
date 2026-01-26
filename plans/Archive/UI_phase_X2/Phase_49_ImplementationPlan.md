# Phase 49: Advanced Portfolio Performance Attribution (Brinson-Fachler UI)

> **Phase ID**: 49 | Status: `[/]` In Progress
> Last Updated: 2026-01-18
> Strategic Importance: Maintains ecosystem accountability by determining if returns are driven by agent skill (Alpha) or mere market exposure (Beta).

---

## Overview

A high-fidelity dashboard for decomposing portfolio returns against benchmarks using the Brinson-Fachler model.

---

## Sub-Deliverable 49.1: Sector Allocation Attribution Widget

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Attribution/SectorAttribution.jsx` | D3.js diverging bar chart |
| `[NEW]` | `frontend2/src/widgets/Attribution/SectorAttribution.css` | Glassmorphism styling |
| `[NEW]` | `frontend2/src/stores/portfolioStore.js` | Attribution state management |
| `[NEW]` | `services/analysis/attribution_service.py` | Brinson-Fachler calculation |
| `[NEW]` | `web/api/attribution_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Brinson-Fachler Decomposition**
   - [ ] Calculate Allocation Effect per GICS sector
   - [ ] Calculate Selection Effect per GICS sector
   - [ ] Calculate Interaction Effect per GICS sector
   - [ ] Sum to Total Active Return

2. **D3.js Diverging Bar Chart**
   - [ ] Hex-scales interpolated for color-blind accessibility
   - [ ] Positive contributions (green) extend right
   - [ ] Negative contributions (red) extend left
   - [ ] Hover tooltip with basis points

3. **Benchmark Comparison**
   - [ ] Support S&P 500, Nasdaq, Custom Index
   - [ ] Real-time comparison (< 50ms state hydration)
   - [ ] Benchmark selector dropdown

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `SectorAttribution.test.jsx` | Chart renders, hover tooltip, benchmark switch |
| `portfolioStore.test.js` | State hydration < 50ms, benchmark change |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_attribution_service.py` | `test_brinson_allocation_effect`, `test_brinson_selection_effect`, `test_brinson_interaction_effect`, `test_total_active_return` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 49.2: Interaction Effect Heatmap (D3.js)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Attribution/InteractionHeatmap.jsx` | SVG matrix visualization |
| `[NEW]` | `frontend2/src/widgets/Attribution/InteractionHeatmap.css` | Styling |

### Verbose Acceptance Criteria

1. **SVG Grid Performance**
   - [ ] Render at 60 FPS during zoom/pan (Framer Motion)
   - [ ] Interpolate hex-colors based on std deviation
   - [ ] Highlight outlier cells (> 2 std dev)

2. **Tooltip Display**
   - [ ] 70% opacity glassmorphism overlay
   - [ ] Show raw interaction effect (basis points)
   - [ ] Show sector pair contribution

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `InteractionHeatmap.test.jsx` | Grid renders, color interpolation, tooltip |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 49.3: Benchmark Relative-Strength Overlay

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Attribution/RelativeStrength.jsx` | Canvas-based chart |
| `[NEW]` | `frontend2/src/widgets/Attribution/RelativeStrength.css` | Styling |

### Verbose Acceptance Criteria

1. **Canvas Rendering**
   - [ ] Handle 10,000+ data points with zero UI jank
   - [ ] HTML5 Canvas for line layer
   - [ ] SVG overlay for annotations

2. **Regime Shift Indicator**
   - [ ] Highlight periods of strategy-benchmark decoupling
   - [ ] Neo4j relationship markers for events
   - [ ] Clickable to see event details

3. **PDF Export**
   - [ ] Offload to Web Worker (no main-thread blocking)
   - [ ] Include all visible charts
   - [ ] SHA-256 integrity hash

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `RelativeStrength.test.jsx` | Canvas renders, regime markers, PDF export |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_attribution_service.py` | `test_regime_shift_detection`, `test_relative_strength_calculation` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/analytics/attribution`

**Macro Task:** Performance Accountability

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Attribution

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_attribution_service.py -v --cov=services/analysis
```

### Integration Tests
```bash
.\venv\Scripts\python.exe -m pytest tests/integration/test_attribution_api.py -v
```

### E2E Browser Tests
```bash
# Stop previous runtimes, start dev server
.\venv\Scripts\python.exe cli.py dev

# Navigate to http://localhost:5173/analytics/attribution
# Verify: Sector chart renders, heatmap displays, benchmark switch works
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 49 detailed implementation plan |
