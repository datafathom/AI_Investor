# Phase 10: Global Macro & Commodities Heatmaps

> **Phase 53** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Monitors the 'Environmental Conditions' (Supply Chains, Politics) that precede price oscillations.

---

## Overview

Mapping of global trade, political alpha, and commodity term structures. Macro conditions are the weather system that determines which sectors will thrive or struggle.

---

## Sub-Deliverable 53.1: Interactive D3 World Map (Shipping & Politics)

### Description
Choropleth map integrating shipping delays and the Nancy Pelosi Index for political alpha detection.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Macro/WorldMap.jsx` | Main map widget |
| `[NEW]` | `frontend2/src/widgets/Macro/WorldMap.css` | Map styling |
| `[NEW]` | `frontend2/src/widgets/Macro/RegionTooltip.jsx` | Region detail tooltip |
| `[NEW]` | `frontend2/src/stores/macroStore.js` | Zustand macro store |
| `[NEW]` | `frontend2/src/services/shippingService.js` | Marine Traffic API |

### Verbose Acceptance Criteria

1. **Neo4j Political Insider Display**
   - [ ] Query `POLITICAL_INSIDER` nodes showing 13F filing locations
   - [ ] Display heat overlay based on filing concentrations
   - [ ] Clickable regions trigger state update to show localized filings
   - [ ] Badge count: "X insider trades in this region"

2. **Shipping Congestion Icons**
   - [ ] Real-time data from Marine Traffic API topics
   - [ ] Port congestion indicators: Green (normal), Yellow (delayed), Red (severe)
   - [ ] Major shipping routes highlighted
   - [ ] Tooltip: "Port of LA: 15 ships waiting, avg delay 4.2 days"

3. **Regional Economic Data**
   - [ ] Click region to show localized CPI/PPI data
   - [ ] Update `useMacroStore` with selected region
   - [ ] Display key metrics: GDP growth, Inflation, Unemployment
   - [ ] Compare to global averages

4. **Map Interactions**
   - [ ] Zoom in/out with mouse wheel
   - [ ] Pan by drag
   - [ ] Reset view button
   - [ ] Toggle layers: Politics, Shipping, Economics

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/macro/political-filings` | GET | Political insider trading data |
| `/api/v1/macro/shipping-congestion` | GET | Port congestion data |
| `/api/v1/macro/regional-economics` | GET | Regional CPI/PPI data |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `WorldMap.test.jsx` | Map renders, click region updates store, layers toggle |
| `RegionTooltip.test.jsx` | Displays correct data, positioning |
| `shippingService.test.js` | API parsing, error handling |
| `macroStore.test.js` | Region selection, layer toggles |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 53.2: Futures Curve Contango/Backwardation Visualizer

### Description
D3.js plotter for the term structure of energy and agricultural futures.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Macro/FuturesCurve.jsx` | Futures curve widget |
| `[NEW]` | `frontend2/src/widgets/Macro/FuturesCurve.css` | Widget styling |
| `[NEW]` | `frontend2/src/widgets/Macro/RollYieldIndicator.jsx` | Roll yield marker |
| `[NEW]` | `frontend2/src/services/futuresService.js` | Futures data service |

### Verbose Acceptance Criteria

1. **Roll Yield Opportunity Markers**
   - [ ] Visual markers on curve where roll yield is attractive
   - [ ] Contango (upward slope) = negative roll yield warning
   - [ ] Backwardation (downward slope) = positive roll yield opportunity
   - [ ] "Roll Cost" calculation for each contract month

2. **Cross-Commodity Spread Charts**
   - [ ] Support common spreads:
     - Crack Spread: Crude vs Gasoline/Heating Oil
     - Crush Spread: Soybeans vs Meal/Oil
     - Spark Spread: Natural Gas vs Electricity
   - [ ] Historical spread overlay
   - [ ] Anomaly detection for spread deviations

3. **Commodity Selection**
   - [ ] Dropdown for common commodities: WTI, Brent, Natural Gas, Gold, Corn, Wheat
   - [ ] Multiple curves on same chart for comparison
   - [ ] Color-coded by commodity type

4. **Latency Requirement**
   - [ ] Futures price updates in <200ms via Kafka
   - [ ] Latency indicator in widget corner
   - [ ] Stale data warning if >1 minute old

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `FuturesCurve.test.jsx` | Curve renders, contango/backwardation detection |
| `RollYieldIndicator.test.jsx` | Markers positioned correctly |
| `futuresService.test.js` | Data parsing, spread calculation |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 53.3: Inflation-Sensitive Asset Correlation Matrix (Neo4j)

### Description
Graph-based visualization of how assets respond to inflationary regimes.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Macro/InflationMatrix.jsx` | Correlation matrix |
| `[NEW]` | `frontend2/src/widgets/Macro/InflationMatrix.css` | Matrix styling |
| `[NEW]` | `frontend2/src/services/neo4jService.js` | Neo4j query service |

### Verbose Acceptance Criteria

1. **Neo4j Edge Relationships**
   - [ ] Map `INFLATION_HEDGE` edges (assets that benefit from inflation)
   - [ ] Map `DEFLATION_VICTIM` edges (assets hurt by deflation)
   - [ ] Edge weight = correlation strength (0 to 1)
   - [ ] Bi-directional relationships supported

2. **Dynamic Clustering**
   - [ ] Cluster assets by sensitivity to 10-year break-even inflation rates
   - [ ] Visual grouping in force-directed layout
   - [ ] Color by cluster: Inflation Hedges (gold), Deflation Victims (red), Neutral (gray)

3. **Query Performance**
   - [ ] Cypher query execution in <150ms
   - [ ] Loading spinner during query
   - [ ] Cache results for 5 minutes
   - [ ] "Refresh" button to force re-query

4. **Interactive Features**
   - [ ] Click node to see asset details
   - [ ] Drag nodes to rearrange
   - [ ] Zoom/pan support
   - [ ] Filter by asset class

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/graph/inflation-matrix` | GET | Neo4j correlation data |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `InflationMatrix.test.jsx` | Matrix renders, nodes clickable, clustering visible |
| `neo4jService.test.js` | Query execution, caching, error handling |

### Test Coverage Target: **80%**

---

## Widget Registry Entries

```javascript
{
  id: 'world-map',
  name: 'Global Macro Map',
  component: lazy(() => import('../../widgets/Macro/WorldMap')),
  category: 'Macro',
  defaultSize: { width: 700, height: 450 }
},
{
  id: 'futures-curve',
  name: 'Futures Term Structure',
  component: lazy(() => import('../../widgets/Macro/FuturesCurve')),
  category: 'Macro',
  defaultSize: { width: 550, height: 350 }
},
{
  id: 'inflation-matrix',
  name: 'Inflation Correlation Matrix',
  component: lazy(() => import('../../widgets/Macro/InflationMatrix')),
  category: 'Macro',
  defaultSize: { width: 500, height: 500 }
}
```

---

## Route Integration

**Route:** `/observer/macro`

**Macro Task:** The Observer

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

