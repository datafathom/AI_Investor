# Phase 6: Portfolio Performance Attribution (Brinson-Fachler)

> **Phase 49** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Maintains ecosystem accountability by determining if returns are driven by agent skill (Alpha) or mere market exposure (Beta).

---

## Overview

A high-fidelity dashboard for decomposing portfolio returns against benchmarks using the **Brinson-Fachler model**. This attribution analysis is critical for understanding whether the AI agents are generating true alpha or simply riding market beta.

---

## Sub-Deliverable 49.1: Sector Allocation Attribution Widget

### Description
Visual breakdown of selection and allocation effects per GICS sector, enabling traders to see exactly where alpha is being generated or destroyed.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Attribution/SectorAttribution.jsx` | Main widget component |
| `[NEW]` | `frontend2/src/widgets/Attribution/SectorAttribution.css` | Widget styling |
| `[NEW]` | `frontend2/src/widgets/Attribution/index.js` | Barrel export |
| `[NEW]` | `frontend2/src/stores/portfolioStore.js` | Zustand store for portfolio state |
| `[NEW]` | `frontend2/src/hooks/useAttributionData.js` | Data fetching hook |
| `[MODIFY]` | `frontend2/src/components/WidgetCatalog/WidgetCatalog.jsx` | Register widget |

### Verbose Acceptance Criteria

1. **Zustand State Management**
   - [ ] Attribution logic triggers partial state re-hydration via `usePortfolioStore`
   - [ ] Benchmark changes reflect in UI in <50ms
   - [ ] State shape: `{ holdings, benchmarks, attributionResults, selectedBenchmark }`

2. **D3.js Diverging Bar Charts**
   - [ ] Implement horizontal diverging bar chart for allocation effect
   - [ ] Implement horizontal diverging bar chart for selection effect
   - [ ] Use hex-scales interpolated for color-blind accessibility (Viridis palette)
   - [ ] Positive values extend right (green tones), negative extend left (red tones)
   - [ ] Bar labels show basis point contribution (+15bps, -8bps)

3. **Multi-Benchmark Support**
   - [ ] Support real-time comparison against 3 concurrent benchmarks
   - [ ] Default benchmarks: S&P 500, Nasdaq Composite, Custom Index
   - [ ] Dropdown selector to add/remove benchmarks
   - [ ] "Custom Index" allows user-defined ETF basket

4. **Sector Breakdown**
   - [ ] All 11 GICS sectors represented
   - [ ] Sectors sorted by absolute attribution impact
   - [ ] Click sector to drill down into top 5 holdings

### Backend Requirements

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| `/api/v1/portfolio/attribution` | POST | `{ portfolioId, benchmarkIds[], dateRange }` | `{ sectors[], totalAlpha, totalBeta }` |
| `/api/v1/benchmarks` | GET | - | `{ benchmarks[] }` |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `SectorAttribution.test.jsx` | Renders all GICS sectors, handles empty data, benchmark selector works |
| `portfolioStore.test.js` | Benchmark change triggers re-hydration, state updates <50ms |
| `useAttributionData.test.js` | API call on mount, error handling, loading states |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 49.2: Interaction Effect Heatmap (D3.js)

### Description
A matrix visualization of the combined impact of allocation and selection choices, revealing cross-sector effects that simple bar charts miss.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Attribution/InteractionHeatmap.jsx` | Heatmap component |
| `[NEW]` | `frontend2/src/widgets/Attribution/InteractionHeatmap.css` | Heatmap styling |
| `[NEW]` | `frontend2/src/utils/colorScales.js` | Shared D3 color scale utilities |

### Verbose Acceptance Criteria

1. **SVG Grid Rendering**
   - [ ] Render 11x11 matrix (sector vs sector interactions)
   - [ ] Maintain 60 FPS during zoom/pan interactions
   - [ ] Use Framer Motion for smooth zoom transitions
   - [ ] Cell size: minimum 40x40px, scales with container

2. **Color Interpolation**
   - [ ] Interpolate hex-colors based on standard deviation of attribution delta
   - [ ] Center color (0 std dev) = neutral gray
   - [ ] Positive outliers = vibrant green
   - [ ] Negative outliers = vibrant red
   - [ ] Legend with continuous gradient scale

3. **Persistent Tooltips**
   - [ ] Hover shows raw basis point contributions
   - [ ] Tooltip includes: Sector A, Sector B, Interaction Effect, Significance
   - [ ] Tooltip persists on click for comparison
   - [ ] Multi-select cells for side-by-side analysis

4. **Outlier Highlighting**
   - [ ] Cells >2 std dev get pulsing border animation
   - [ ] "Anomaly Alert" badge when interaction effect exceeds thresholds

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `InteractionHeatmap.test.jsx` | SVG renders 121 cells, color scale applies, tooltip on hover |
| `colorScales.test.js` | Std dev calculation correct, color interpolation boundary cases |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 49.3: Benchmark Relative-Strength Overlay

### Description
A zero-lag chart comparing the strategy's equity curve against institutional indices, with regime-shift detection to identify when the strategy decouples from markets.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Attribution/RelativeStrength.jsx` | Chart component |
| `[NEW]` | `frontend2/src/widgets/Attribution/RelativeStrength.css` | Chart styling |
| `[NEW]` | `frontend2/src/workers/pdfExport.worker.js` | Web Worker for PDF generation |
| `[NEW]` | `frontend2/src/hooks/useCanvasChart.js` | Canvas rendering hook |

### Verbose Acceptance Criteria

1. **HTML5 Canvas Rendering**
   - [ ] Handle 10,000+ data points without frame drops
   - [ ] Use Canvas for the line layer (not SVG for performance)
   - [ ] Maintain 60 FPS during pan/zoom
   - [ ] Downsampling algorithm for dense data (LTTB or similar)

2. **Regime Shift Indicator**
   - [ ] Detect periods when strategy-to-benchmark correlation breaks
   - [ ] Visual highlight (shaded region) during decoupling periods
   - [ ] Correlation threshold: <0.5 for 10+ consecutive days
   - [ ] Annotate with "Regime Shift Detected" label

3. **Multi-Line Display**
   - [ ] Strategy equity curve (primary, bold)
   - [ ] Up to 3 benchmark curves (secondary, thinner)
   - [ ] Legend with real-time values on hover
   - [ ] Toggle individual lines on/off

4. **PDF Report Generation**
   - [ ] "Export PDF" button triggers background worker
   - [ ] Worker generates chart image + statistics table
   - [ ] UI shows progress indicator, remains responsive
   - [ ] PDF includes: Chart, Date Range, Key Metrics, Regime Annotations

### Backend Requirements

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| `/api/v1/portfolio/equity-curve` | GET | `?portfolioId=X&startDate=Y&endDate=Z` | `{ dates[], values[], benchmarks[] }` |
| `/api/v1/analytics/regime-shifts` | GET | `?portfolioId=X` | `{ shifts[{ start, end, correlation }] }` |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `RelativeStrength.test.jsx` | Canvas renders, handles 10k points, regime highlight appears |
| `useCanvasChart.test.js` | Downsampling works, zoom state management |
| `pdfExport.worker.test.js` | Worker generates blob, handles errors |

### Test Coverage Target: **80%**

---

## Widget Registry Entry

```javascript
// Add to frontend2/src/components/WidgetCatalog/widgets.js
{
  id: 'attribution-sector',
  name: 'Sector Attribution',
  component: lazy(() => import('../../widgets/Attribution/SectorAttribution')),
  category: 'Portfolio',
  defaultSize: { width: 500, height: 400 },
  minSize: { width: 350, height: 300 }
},
{
  id: 'attribution-heatmap',
  name: 'Interaction Heatmap',
  component: lazy(() => import('../../widgets/Attribution/InteractionHeatmap')),
  category: 'Portfolio',
  defaultSize: { width: 450, height: 450 },
  minSize: { width: 350, height: 350 }
},
{
  id: 'relative-strength',
  name: 'Relative Strength',
  component: lazy(() => import('../../widgets/Attribution/RelativeStrength')),
  category: 'Portfolio',
  defaultSize: { width: 600, height: 350 },
  minSize: { width: 400, height: 250 }
}
```

---

## Route Integration

**Route:** `/strategist/portfolio/attribution`

**Macro Task:** The Strategist

**Default Layout:**
- SectorAttribution (left, 50% width)
- InteractionHeatmap (top-right, 25% width)
- RelativeStrength (bottom-right, 25% width, spanning full width)

---

## Dependencies

- D3.js ^7.x
- Framer Motion ^10.x
- react-window (for virtualized lists if needed)
- Web Worker support (all modern browsers)

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

