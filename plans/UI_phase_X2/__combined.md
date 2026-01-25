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


---

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


---

# Phase 51: Multi-Asset Cryptographic Vaulting & Web3 GUI

> **Phase ID**: 51 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Integrates decentralized 'Metabolism' metrics (gas, liquidity) into the centralized homeostasis model.

---

## Overview

Interface for cold/hot wallet orchestration and DeFi position tracking.

---

## Sub-Deliverable 51.1: Hardware Wallet Connectivity Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Web3/WalletDashboard.jsx` | Ledger/Trezor monitor |
| `[NEW]` | `frontend2/src/widgets/Web3/WalletDashboard.css` | Styling |
| `[NEW]` | `frontend2/src/stores/web3Store.js` | Web3 state management |
| `[NEW]` | `services/crypto/wallet_service.py` | Wallet connectivity |
| `[NEW]` | `web/api/web3_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **WebSocket Connectivity**
   - [ ] > 99.9% uptime with automated retry logic
   - [ ] Connection status indicator
   - [ ] Multi-chain support (ETH, BTC, SOL)

2. **Security Masking**
   - [ ] Public keys masked by default
   - [ ] WebAuthn/OAuth 2.0 biometric reveal
   - [ ] Session timeout (5 min inactivity)

3. **Real-time Valuation**
   - [ ] Kafka-driven price feeds
   - [ ] Multi-exchange weighting (Binance, Coinbase, Kraken)
   - [ ] USD/EUR/BTC toggle

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `WalletDashboard.test.jsx` | Connection status, masking, valuation update |
| `web3Store.test.js` | State persistence, biometric flow mock |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/crypto/test_wallet_service.py` | `test_websocket_retry`, `test_multi_chain_balance`, `test_price_aggregation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 51.2: On-chain Liquidity Provider (LP) Position Tracker

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Web3/LPTracker.jsx` | LP position viewer |
| `[NEW]` | `frontend2/src/widgets/Web3/LPTracker.css` | Styling |
| `[NEW]` | `services/crypto/lp_tracker_service.py` | Impermanent loss calc |

### Verbose Acceptance Criteria

1. **Impermanent Loss Visualization**
   - [ ] D3.js chart: 'HODL Value' vs 'LP Value' over time
   - [ ] Percentage loss/gain display
   - [ ] Break-even marker

2. **Pool Drain Detection**
   - [ ] Abnormal slippage telemetry via Kafka
   - [ ] Auto-alert on pool imbalance
   - [ ] Exit recommendation

3. **Neo4j Mapping**
   - [ ] `LIQUIDITY_SOURCE` relationships to tokens
   - [ ] Correlation analysis edges
   - [ ] Graph visualization option

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `LPTracker.test.jsx` | IL chart renders, drain alert, graph toggle |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/crypto/test_lp_tracker_service.py` | `test_impermanent_loss_calc`, `test_pool_drain_detection`, `test_neo4j_mapping` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 51.3: Gas Fee Optimization & Speed Controller

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Web3/GasPulse.jsx` | Real-time Gwei monitor |
| `[NEW]` | `frontend2/src/widgets/Web3/GasPulse.css` | Styling |
| `[NEW]` | `services/crypto/gas_service.py` | Gas optimization |

### Verbose Acceptance Criteria

1. **Gwei Pulse Widget**
   - [ ] Real-time gas price display
   - [ ] Historical 24h moving average overlay
   - [ ] Color-coded urgency (low/medium/high)

2. **Meta-Transaction Builder**
   - [ ] Zustand-based transaction queue
   - [ ] Queue trades for gas troughs
   - [ ] Estimated savings display

3. **Spike Alerts**
   - [ ] Alert when gas > 3 std dev of 24h mean
   - [ ] Push notification option
   - [ ] Auto-pause pending transactions

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `GasPulse.test.jsx` | Pulse renders, queue works, spike alert |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/crypto/test_gas_service.py` | `test_gas_fetch`, `test_spike_detection`, `test_queue_optimization` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/portfolio/web3`

**Macro Task:** Decentralized Metabolism

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Web3

# Backend
.\venv\Scripts\python.exe -m pytest tests/crypto/ -v --cov=services/crypto
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/portfolio/web3
# Verify: Wallet connects (mock), LP tracker shows, gas pulse updates
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 51 detailed implementation plan |


---

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


---

# Phase 53: Global Macro & Commodities Heatmaps

> **Phase ID**: 53 | Status: `[ ]` Not Started
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


---

# Phase 54: Institutional KYC & Secure Document Vault

> **Phase ID**: 54 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Establishes the 'Fort Knox' legal boundary required for institutional-scale operation.

---

## Overview

Secure identity management and encrypted document orchestration.

---

## Sub-Deliverable 54.1: Encrypted Identity Verification Portal

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/KYC/VerificationPortal.jsx` | Secure upload portal |
| `[NEW]` | `frontend2/src/widgets/KYC/VerificationPortal.css` | Styling |
| `[NEW]` | `frontend2/src/stores/kycStore.js` | KYC state management |
| `[NEW]` | `services/security/kyc_service.py` | KYC verification logic |
| `[NEW]` | `web/api/kyc_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **E2E Encryption**
   - [ ] AES-256 client-side encryption before upload
   - [ ] Key derivation from user biometric
   - [ ] Zero-knowledge storage

2. **Verification Status**
   - [ ] Real-time progress bars (Zustand)
   - [ ] Kafka status updates
   - [ ] Email/SMS notifications

3. **Third-Party Integration**
   - [ ] Plaid API for bank verification
   - [ ] Jumio API for ID verification
   - [ ] Secure webhook handlers

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `VerificationPortal.test.jsx` | Upload works, progress updates, encryption mock |
| `kycStore.test.js` | Status tracking, multi-step flow |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_kyc_service.py` | `test_encryption_integrity`, `test_plaid_integration`, `test_jumio_webhook` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 54.2: Audit-Trail Document Management System

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/KYC/DocumentVault.jsx` | Version-controlled vault |
| `[NEW]` | `frontend2/src/widgets/KYC/DocumentVault.css` | Styling |
| `[NEW]` | `services/security/vault_service.py` | Document management |

### Verbose Acceptance Criteria

1. **Immutable Logging**
   - [ ] Every access logged to `UnifiedActivityService`
   - [ ] Timestamps with user ID
   - [ ] Cannot be deleted or modified

2. **Full-Text Search**
   - [ ] Postgres full-text indexing on metadata
   - [ ] Filter by document type, date, entity
   - [ ] Instant results (< 100ms)

3. **RBAC Enforcement**
   - [ ] Role-based access at component level
   - [ ] React Context enforcement
   - [ ] Admin/Viewer/Owner roles

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DocumentVault.test.jsx` | Document list, search, RBAC enforcement |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_vault_service.py` | `test_audit_immutability`, `test_fulltext_search`, `test_rbac_enforcement` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 54.3: Regulatory Filing Progress Tracker (13F, etc.)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/KYC/FilingTracker.jsx` | 13F deadline tracker |
| `[NEW]` | `frontend2/src/widgets/KYC/FilingTracker.css` | Styling |

### Verbose Acceptance Criteria

1. **SEC Calendar Integration**
   - [ ] Automated 13F filing window alerts
   - [ ] Taskbar notification integration
   - [ ] Email reminders T-30, T-7, T-1

2. **Data Readiness**
   - [ ] Visual indicator based on transaction volume
   - [ ] Missing data warnings
   - [ ] Completeness percentage

3. **XML Export**
   - [ ] SEC-compliant XML format
   - [ ] Automated validation
   - [ ] One-click export

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `FilingTracker.test.jsx` | Calendar renders, alerts work, export |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_kyc_service.py` | `test_13f_calendar`, `test_xml_generation`, `test_sec_validation` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/guardian/compliance`

**Macro Task:** Fort Knox Legal Boundary

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=KYC

# Backend
.\venv\Scripts\python.exe -m pytest tests/security/ -v --cov=services/security
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/guardian/compliance
# Verify: Upload portal works, vault accessible, tracker shows calendar
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 54 detailed implementation plan |


---

# Phase 55: The Debate Chamber 2.0 (Interactive Persona GUI)

> **Phase ID**: 55 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Exposes the internal 'Swarm Logic' to the user to reduce groupthink and validate intent.

---

## Overview

A visual interface for the multi-persona LLM committee debate process.

---

## Sub-Deliverable 55.1: Multi-Agent Chat Interface (Bull vs. Bear)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/AgentChat.jsx` | Real-time debate stream |
| `[NEW]` | `frontend2/src/widgets/Debate/AgentChat.css` | Styling |
| `[MODIFY]` | `frontend2/src/stores/debateStore.js` | Enhanced debate state |
| `[NEW]` | `services/agents/debate_orchestrator.py` | Multi-agent coordination |
| `[MODIFY]` | `web/api/debate_api.py` | Enhanced endpoints |

### Verbose Acceptance Criteria

1. **Persona Avatars**
   - [ ] Tailwind color-coded 'Sentiment Glow' (Green Bull, Red Bear)
   - [ ] Unique avatar per persona (Searcher, Protector, Stacker)
   - [ ] Typing indicator animation

2. **User Injection**
   - [ ] 'Branch' button to inject counter-arguments
   - [ ] Arguments added to LLM context
   - [ ] Response regeneration

3. **Persistence**
   - [ ] Messages tagged with `PERSONA_ID`
   - [ ] Stored in `useDebateStore`
   - [ ] Export conversation history

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `AgentChat.test.jsx` | Personas render, injection works, history persists |
| `debateStore.test.js` | Message tagging, export function |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/agents/test_debate_orchestrator.py` | `test_multi_agent_coordination`, `test_argument_injection`, `test_consensus_calculation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 55.2: Voting/Consensus Progress Bar

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/ConsensusBar.jsx` | Agreement visualizer |
| `[NEW]` | `frontend2/src/widgets/Debate/ConsensusBar.css` | Styling |

### Verbose Acceptance Criteria

1. **70% Threshold**
   - [ ] 'Approve Execution' locked until 70% consensus
   - [ ] Visual progress bar
   - [ ] Animated vote changes

2. **Dissent Display**
   - [ ] Dissenting agents highlighted
   - [ ] Hover tooltip with 'Reason for Dissent'
   - [ ] LLM-derived reasoning

3. **Real-time Updates**
   - [ ] Zustand state updates instantly
   - [ ] WebSocket for live debate
   - [ ] Vote change history

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ConsensusBar.test.jsx` | Progress renders, threshold enforced, dissent tooltip |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 55.3: Argument Mapping Tree (Neo4j)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/ArgumentTree.jsx` | Graph visualization |
| `[NEW]` | `frontend2/src/widgets/Debate/ArgumentTree.css` | Styling |

### Verbose Acceptance Criteria

1. **Neo4j Edge Mapping**
   - [ ] `PRO_ARGUMENT` edges between hypothesis and evidence
   - [ ] `CON_ARGUMENT` edges for counterpoints
   - [ ] Clickable nodes

2. **Confidence Weights**
   - [ ] Edge weights from LLM confidence scores (0.0-1.0)
   - [ ] Visual thickness based on weight
   - [ ] Filter by confidence threshold

3. **Source Links**
   - [ ] Fact-nodes link to source news
   - [ ] Social sentiment spike references
   - [ ] SEC filing citations

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ArgumentTree.test.jsx` | Graph renders, edges weighted, source links work |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/agents/test_debate_orchestrator.py` | `test_argument_graph_generation`, `test_confidence_weighting`, `test_source_linking` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/workspace/debate`

**Macro Task:** Swarm Logic Exposure

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Debate

# Backend
.\venv\Scripts\python.exe -m pytest tests/agents/test_debate_orchestrator.py -v --cov=services/agents
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/workspace/debate
# Verify: Chat shows personas, consensus bar updates, graph is interactive
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 55 detailed implementation plan |


---

# Phase 56: Multi-Currency Cash Management & FX Conversion

> **Phase ID**: 56 | Status: `[ ]` Not Started
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


---

# Phase 57: Advanced Backtest Result Explorer (V2)

> **Phase ID**: 57 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Uses 10,000 parallel realities to ensure the current strategy is not an outlier and avoids extinction.

---

## Overview

Deep-dive statistical explorer for historical simulation results.

---

## Sub-Deliverable 57.1: Monte Carlo Simulation Path Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/MonteCarloViz.jsx` | Canvas-based paths |
| `[NEW]` | `frontend2/src/widgets/Backtest/MonteCarloViz.css` | Styling |
| `[MODIFY]` | `frontend2/src/stores/backtestStore.js` | Enhanced state |
| `[NEW]` | `services/analysis/monte_carlo_service.py` | GBM simulation |
| `[MODIFY]` | `web/api/backtest_api.py` | Enhanced endpoints |

### Verbose Acceptance Criteria

1. **10k Path Rendering**
   - [ ] HTML5 Canvas at 60 FPS
   - [ ] Quantile shading (5/50/95%)
   - [ ] Geometric Brownian Motion (GBM)

2. **Probability of Ruin**
   - [ ] Based on user-defined drawdown limits
   - [ ] Visual 'Extinction Event' marker
   - [ ] Percentage display

3. **Interactive Sliders**
   - [ ] Adjust volatility (sigma) in real-time
   - [ ] Adjust drift (mu) in real-time
   - [ ] See path shifts instantly

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `MonteCarloViz.test.jsx` | Paths render, quantiles display, sliders work |
| `backtestStore.test.js` | Simulation params persist |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_monte_carlo_service.py` | `test_gbm_simulation`, `test_ruin_probability`, `test_quantile_calculation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 57.2: Maximum Drawdown 'Stress Point' Timeline

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/DrawdownTimeline.jsx` | Annotated timeline |
| `[NEW]` | `frontend2/src/widgets/Backtest/DrawdownTimeline.css` | Styling |

### Verbose Acceptance Criteria

1. **Event Annotations**
   - [ ] Link to `MACRO_EVENT` nodes in Neo4j
   - [ ] '2020 C19 Crash', '2008 Financial Crisis' labels
   - [ ] Clickable for details

2. **Underwater Chart**
   - [ ] Time-to-recovery in days
   - [ ] Depth visualization
   - [ ] Current vs historical comparison

3. **Risk Metrics**
   - [ ] Ulcer Index calculation
   - [ ] Pain Index (duration × depth)
   - [ ] Rolling max drawdown

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DrawdownTimeline.test.jsx` | Timeline renders, events annotated, metrics display |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_monte_carlo_service.py` | `test_drawdown_calculation`, `test_ulcer_index`, `test_recovery_time` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 57.3: Out-of-Sample Performance Variance Matrix

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Backtest/VarianceMatrix.jsx` | Overfit detector |
| `[NEW]` | `frontend2/src/widgets/Backtest/VarianceMatrix.css` | Styling |

### Verbose Acceptance Criteria

1. **Overfit Warning**
   - [ ] Visual alert if IS vs OOS Sharpe variance > 20%
   - [ ] Red border warning
   - [ ] Explanation tooltip

2. **Ratio Comparison**
   - [ ] Sharpe, Sortino, Calmar per yearly bucket
   - [ ] Side-by-side table
   - [ ] Historical trend lines

3. **Parameter Sharing**
   - [ ] Zustand persistence for backtest params
   - [ ] Easy sharing across agent swarms
   - [ ] URL-encoded params

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `VarianceMatrix.test.jsx` | Matrix renders, overfit warning, ratio comparison |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_monte_carlo_service.py` | `test_sharpe_calculation`, `test_overfit_detection`, `test_param_serialization` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/analyst/backtest`

**Macro Task:** Robustness Verification

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Backtest

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_monte_carlo_service.py -v --cov=services/analysis
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/analyst/backtest
# Verify: 10k paths render smoothly, drawdown annotated, overfit detector works
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 57 detailed implementation plan |


---

# Phase 58: Estate Planning & Inheritance Protocol Wizard

> **Phase ID**: 58 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Extends the 'Life' of the financial ecosystem beyond the primary warden.

---

## Overview

Configurator for succession logic and the 'Dead Man's Switch'.

---

## Sub-Deliverable 58.1: Dead Man's Switch Configuration Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/DeadManSwitch.jsx` | Safety mechanism |
| `[NEW]` | `frontend2/src/widgets/Estate/DeadManSwitch.css` | Styling |
| `[NEW]` | `frontend2/src/stores/estateStore.js` | Estate state management |
| `[NEW]` | `services/security/estate_service.py` | Succession logic |
| `[NEW]` | `web/api/estate_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Countdown Timer**
   - [ ] Visual 'Time to Trigger' with high-contrast colors
   - [ ] Configurable heartbeat interval (7-90 days)
   - [ ] Reset on any platform activity

2. **Multi-Channel Verification**
   - [ ] SMS, Email, App push for heartbeat
   - [ ] Configurable channels
   - [ ] Fallback chain

3. **Encrypted Beneficiary Keys**
   - [ ] Keys encrypted until trigger fires
   - [ ] Verified via immutable audit log
   - [ ] Multi-sig option for high-value estates

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DeadManSwitch.test.jsx` | Countdown displays, reset works, channels configurable |
| `estateStore.test.js` | Timer persistence, trigger logic |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_estate_service.py` | `test_heartbeat_detection`, `test_key_encryption`, `test_trigger_execution` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 58.2: Beneficiary Asset Allocation Mapping

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryTree.jsx` | Allocation tree |
| `[NEW]` | `frontend2/src/widgets/Estate/BeneficiaryTree.css` | Styling |

### Verbose Acceptance Criteria

1. **Drag-and-Drop Allocation**
   - [ ] Percentage balance checking (must sum to 100%)
   - [ ] Real-time validation
   - [ ] Visual split indicators

2. **Document Vault Linking**
   - [ ] Link specific assets to Trust deeds
   - [ ] Corporate resolution references
   - [ ] Document status indicators

3. **Estate Tax Simulation**
   - [ ] Per-beneficiary tax impact
   - [ ] Based on jurisdictional law
   - [ ] What-if scenarios

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BeneficiaryTree.test.jsx` | Drag works, percentages validate, tax displays |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_estate_service.py` | `test_allocation_validation`, `test_tax_calculation`, `test_document_linking` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 58.3: Trust/Entity Legal Structure Visualizer (Neo4j)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Estate/EntityGraph.jsx` | Graph visualization |
| `[NEW]` | `frontend2/src/widgets/Estate/EntityGraph.css` | Styling |

### Verbose Acceptance Criteria

1. **Node Types**
   - [ ] `ENTITY`, `TRUST`, `INDIVIDUAL` node types
   - [ ] `OWNS`, `BENEFICIARY_OF` edge types
   - [ ] Color-coded by type

2. **Hover Details**
   - [ ] Tax ID display
   - [ ] Jurisdiction (Delaware LLC, Wyoming Trust)
   - [ ] Formation date

3. **Corporate Resolution Generator**
   - [ ] One-click generation for structural changes
   - [ ] Stored in Document Vault
   - [ ] Template library

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EntityGraph.test.jsx` | Graph renders, hover works, resolution generates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/security/test_estate_service.py` | `test_entity_graph_query`, `test_resolution_template`, `test_vault_storage` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/estate`

**Macro Task:** Ecosystem Life Extension

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Estate

# Backend
.\venv\Scripts\python.exe -m pytest tests/security/test_estate_service.py -v --cov=services/security
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/strategist/estate
# Verify: Dead man's switch configurable, allocation tree works, entity graph displays
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 58 detailed implementation plan |


---

# Phase 59: Regulatory Compliance & Audit Log Explorer

> **Phase ID**: 59 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Ensures the system remains a 'Lawful Predator' within the market ecosystem.

---

## Overview

Forensic explorer for all trading activity and automated reporting. This phase establishes the regulatory compliance infrastructure that allows the system to operate at institutional scale while maintaining full transparency and auditability.

---

## Sub-Deliverable 59.1: Real-time 'Anti-Market Abuse' Monitoring Feed

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Compliance/AbuseMonitor.jsx` | Real-time detection feed |
| `[NEW]` | `frontend2/src/widgets/Compliance/AbuseMonitor.css` | Glassmorphism styling |
| `[NEW]` | `frontend2/src/stores/complianceStore.js` | Compliance state management |
| `[NEW]` | `services/compliance/abuse_detection_service.py` | Pattern detection engine |
| `[NEW]` | `web/api/compliance_api.py` | REST endpoints |

### UI/UX Design Specifications

#### Visual Layout
```
┌─────────────────────────────────────────────────────────────┐
│  🛡️ Market Abuse Monitor                    [Live] [Pause]  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 10:42:31 │ ⚪ NORMAL    │ AAPL Buy 100 @ $185.42       ││
│  │ 10:42:33 │ 🟡 FLAGGED   │ TSLA Cancel within 8ms       ││
│  │ 10:42:35 │ 🔴 SPOOFING? │ GME Layered orders detected  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  [Clear Flags]  [Export Report]  [Configure Thresholds]     │
└─────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Scrolling Feed**: Newest entries appear at top with smooth slide-in animation (Framer Motion, 200ms ease-out)
- **Color Coding**: 
  - ⚪ White/Gray: Normal activity (opacity 0.6)
  - 🟡 Yellow pulse: Flagged for review (border-left: 3px solid #FCD34D)
  - 🔴 Red glow: Potential abuse pattern (box-shadow: 0 0 10px rgba(239,68,68,0.5))
- **Hover State**: Expand row to show full order details, historical pattern matches
- **Click Action**: Open detailed investigation modal with timeline reconstruction

#### Glassmorphism Container
```css
.abuse-monitor {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}
```

### Verbose Acceptance Criteria

1. **Spoofing Detection Heuristics**
   - [ ] Flag order cancellations within 10ms of placement
   - [ ] Track cancel-to-fill ratio per session (alert if > 90%)
   - [ ] Visual timeline showing order lifecycle
   - [ ] One-click false-positive marking with reason dropdown

2. **Layering Pattern Recognition**
   - [ ] Detect multiple orders at incrementing price levels
   - [ ] Visual 'ladder' representation of suspected layering
   - [ ] Calculate market impact of detected patterns
   - [ ] Historical comparison to known layering cases

3. **Wash Trading Detection**
   - [ ] Flag circular trades within same beneficial owner
   - [ ] Auto-pause agents engaging in repetitive outlier behavior
   - [ ] Visual connection lines between related accounts
   - [ ] Configurable sensitivity thresholds

4. **Real-time Alert System**
   - [ ] Taskbar notification badge with count
   - [ ] Desktop push notifications for Critical flags
   - [ ] Email digest option (hourly/daily)
   - [ ] Webhook integration for external SIEM

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `AbuseMonitor.test.jsx` | Feed renders, color coding correct, hover expands, filters work |
| `complianceStore.test.js` | Flags persist, thresholds configurable, pause function |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/compliance/test_abuse_detection_service.py` | `test_spoofing_detection_10ms`, `test_layering_pattern`, `test_wash_trade_circular`, `test_agent_pause_trigger` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 59.2: Immutable Activity Audit Log

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Compliance/AuditLogExplorer.jsx` | Forensic log viewer |
| `[NEW]` | `frontend2/src/widgets/Compliance/AuditLogExplorer.css` | Styling |

### UI/UX Design Specifications

#### Visual Layout
```
┌─────────────────────────────────────────────────────────────────────┐
│  📜 Audit Log Explorer                                              │
├─────────────────────────────────────────────────────────────────────┤
│  Filters: [Agent ▼] [Asset Class ▼] [Date Range 📅] [🔍 Search]     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Timestamp          │ Agent      │ Action     │ Details    │ 🔗│  │
│  ├────────────────────┼────────────┼────────────┼────────────┼───┤  │
│  │ 2026-01-18 10:42:31│ StackerBot │ BUY_ORDER  │ AAPL x100  │ ⛓ │  │
│  │ 2026-01-18 10:42:32│ Protector  │ RISK_CHECK │ Passed     │ ⛓ │  │
│  │ 2026-01-18 10:42:33│ System     │ LOG_HASH   │ SHA256:a1b2│ ⛓ │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Showing 1-50 of 12,847 entries    [◀ Prev] [Page 1 of 257] [Next ▶]│
│                                                                      │
│  [🔐 Verify Integrity]  [📦 Export Audit Pack]  [📊 Generate Report] │
└─────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Virtualized Scrolling**: Handle 100k+ entries without UI jank (react-window)
- **Column Sorting**: Click headers to sort, shift+click for secondary sort
- **Inline Expansion**: Click row to expand with full JSON payload
- **Chain Icon (⛓)**: Visual indicator of cryptographic chain integrity
- **Integrity Verification**: Click "Verify Integrity" to validate SHA-256 chain

### Verbose Acceptance Criteria

1. **Cryptographic Integrity**
   - [ ] SHA-256 hash chain for all log entries
   - [ ] Visual chain-link icon (green ✓ valid, red ✗ broken)
   - [ ] One-click full chain verification
   - [ ] Tamper detection alert

2. **Advanced Filtering**
   - [ ] Filter by `AGENT_ID` (multi-select dropdown)
   - [ ] Filter by `ASSET_CLASS` (Equity, Options, Crypto, FX)
   - [ ] Filter by `TIMESTAMP` range (calendar picker)
   - [ ] Full-text search with < 100ms response

3. **Audit Pack Export**
   - [ ] Encrypted ZIP format for regulatory inquiries
   - [ ] Include selected date range only
   - [ ] SHA-256 manifest of all included files
   - [ ] Password protection option (FINRA/SEC compliant)

4. **Performance Requirements**
   - [ ] Query time < 100ms for any filter combination
   - [ ] Pagination with 50/100/500 per page options
   - [ ] Export large datasets via background worker

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `AuditLogExplorer.test.jsx` | Filters work, pagination, export triggers, integrity check |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/compliance/test_audit_service.py` | `test_hash_chain_integrity`, `test_query_performance_100ms`, `test_encrypted_export`, `test_tamper_detection` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 59.3: SAR (Suspicious Activity Report) Automated Flagging UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Compliance/SARWorkflow.jsx` | Case management |
| `[NEW]` | `frontend2/src/widgets/Compliance/SARWorkflow.css` | Styling |

### UI/UX Design Specifications

#### Kanban Layout
```
┌───────────────────────────────────────────────────────────────────────┐
│  📋 SAR Case Management                          [+ New Case] [Filter]│
├───────────────────────────────────────────────────────────────────────┤
│  🔴 NEW (3)        │ 🟡 REVIEW (5)      │ 🟢 FILED (12)   │ ⚫ CLOSED │
│  ┌──────────────┐  │ ┌──────────────┐   │ ┌─────────────┐ │           │
│  │ CASE-2026-42 │  │ │ CASE-2026-38 │   │ │CASE-2026-21 │ │           │
│  │ $125,000 wire│  │ │ Pattern match│   │ │ Filed 01/15 │ │           │
│  │ 🕐 2h ago    │  │ │ 🕐 3d review │   │ │ ✓ Confirmed │ │           │
│  │ [Assign]     │  │ │ [→ File]     │   │ │ [Archive]   │ │           │
│  └──────────────┘  │ └──────────────┘   │ └─────────────┘ │           │
└───────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Drag-and-Drop**: Move cards between columns (Framer Motion drag)
- **Card Expansion**: Click to open full case details in slide-over panel
- **Quick Actions**: Hover reveals action buttons (Assign, Escalate, Close)
- **Time Indicators**: Relative time since creation, color-coded urgency

### Verbose Acceptance Criteria

1. **Automated Draft Generation**
   - [ ] Pre-fill FinCEN Form 111 (SAR) from detected data
   - [ ] Include PII from linked accounts
   - [ ] Summarize transaction volume and patterns
   - [ ] Attach relevant audit log excerpts

2. **False Positive Management**
   - [ ] Manual override interface for machine-detected anomalies
   - [ ] Required 'Reason for Dismissal' dropdown
   - [ ] Audit trail of all dismissal decisions
   - [ ] ML feedback loop for improved detection

3. **Workflow Automation**
   - [ ] Kanban-style case progression
   - [ ] Auto-assign based on case type rules
   - [ ] Escalation path to compliance officer
   - [ ] SLA timers with visual warnings

4. **Filing Integration**
   - [ ] One-click FinCEN e-filing (sandbox mode available)
   - [ ] Confirmation receipt storage
   - [ ] Auto-archive on successful filing
   - [ ] Reopening workflow for amendments

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `SARWorkflow.test.jsx` | Kanban drag works, case opens, draft generates, filing triggers |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/compliance/test_sar_service.py` | `test_auto_draft_generation`, `test_false_positive_logging`, `test_workflow_state_machine`, `test_fincen_format_validation` |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/guardian/audit`

**Macro Task:** Lawful Predator Assurance

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Compliance

# Backend
.\venv\Scripts\python.exe -m pytest tests/compliance/ -v --cov=services/compliance
```

### Integration Tests
```bash
.\venv\Scripts\python.exe -m pytest tests/integration/test_compliance_workflow.py -v
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/guardian/audit
# Verify: Abuse monitor streams, audit log filters, SAR kanban drags
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 59 with enhanced UI/UX verbosity |


---

# Phase 60: Scenario Modeling & 'What-If' Impact Simulator

> **Phase ID**: 60 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Anticipates 'Black Swan' shocks by stress-testing the Yellowstone equilibrium.

---

## Overview

Interactive 'Torture Chamber' for simulating extreme macro shifts. This phase provides the warden with the ability to stress-test portfolio resilience against catastrophic scenarios before they occur, enabling proactive hedging decisions.

---

## Sub-Deliverable 60.1: Drag-and-Drop Macro Event Trigger

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/EventTrigger.jsx` | Macro shock interface |
| `[NEW]` | `frontend2/src/widgets/Scenario/EventTrigger.css` | Glassmorphism styling |
| `[NEW]` | `frontend2/src/stores/scenarioStore.js` | Scenario state management |
| `[NEW]` | `services/analysis/scenario_service.py` | Shock propagation engine |
| `[NEW]` | `web/api/scenario_api.py` | REST endpoints |

### UI/UX Design Specifications

#### Visual Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌪️ Scenario Torture Chamber                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Available Shocks (Drag onto Portfolio)                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🛢️ Oil   │ │ 📈 Fed   │ │ 🦠 Pandemic│ │ 💣 Geo-  │ │ 🏦 Bank  │       │
│  │ $150/bbl │ │ +200bps  │ │ Lockdown │ │ political│ │ Failure │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│        ↓ Drag Here ↓                                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                    │  │
│  │   📊 PORTFOLIO IMPACT ZONE                                        │  │
│  │                                                                    │  │
│  │   Net Worth: $2,450,000  →  $1,892,000 (-22.8%)                   │  │
│  │                                                                    │  │
│  │   🛡️ Hedge Coverage: 68% (Insufficient for this shock)            │  │
│  │                                                                    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  [Reset] [Save Scenario] [Apply Hedge Recommendations]                   │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Drag Initiation**: Touch/click-hold on shock card (0.2s delay to prevent accidental)
- **Drop Zone Feedback**: Glow effect on portfolio zone when dragging over (box-shadow pulse)
- **Impact Animation**: Numbers animate from current → shocked value (CountUp.js, 1.5s)
- **Shake Effect**: Portfolio container shakes briefly on large shocks (> 15% impact)
- **Undo Gesture**: Swipe right on applied shock to remove, or shake device (mobile)

#### Shock Card Design
```css
.shock-card {
  width: 100px;
  height: 80px;
  background: linear-gradient(135deg, rgba(239,68,68,0.3), rgba(239,68,68,0.1));
  border: 1px solid rgba(239,68,68,0.5);
  border-radius: 8px;
  cursor: grab;
  transition: transform 0.2s, box-shadow 0.2s;
}
.shock-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(239,68,68,0.3);
}
.shock-card.dragging {
  cursor: grabbing;
  opacity: 0.8;
  transform: scale(1.05) rotate(-2deg);
}
```

### Verbose Acceptance Criteria

1. **Neo4j Correlation Propagation**
   - [ ] Shock propagates through correlation graph (Oil → Airlines, Energy, Transport)
   - [ ] Visual highlighting of affected sectors on graph
   - [ ] Cascade intensity based on edge weights
   - [ ] Second-order effects visualization (Airlines → Tourism → Hotels)

2. **Real-time Net Worth Impact**
   - [ ] Header displays shocked Net Worth instantly
   - [ ] Delta shown as both absolute and percentage
   - [ ] Color coding: Red (>10% loss), Yellow (5-10%), Green (<5%)
   - [ ] Historical comparison: "Worse than 2008?" indicator

3. **Hedge Sufficiency Indicator**
   - [ ] Visual 'Shield' icon with fill level (0-100%)
   - [ ] Green glow if hedges absorb shock
   - [ ] Red pulse if hedges insufficient
   - [ ] One-click hedge recommendations

4. **Custom Shock Builder**
   - [ ] Create custom shocks with multiple parameters
   - [ ] Save custom shocks to library
   - [ ] Share scenarios with team members
   - [ ] Import historical black swan templates

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `EventTrigger.test.jsx` | Drag works, drop calculates impact, animation plays, reset clears |
| `scenarioStore.test.js` | Shock propagation, hedge calculation, custom shock saving |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_scenario_service.py` | `test_correlation_propagation`, `test_impact_calculation`, `test_hedge_sufficiency`, `test_custom_shock_persistence` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 60.2: Portfolio Revaluation Forecast Chart (Framer Motion)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/ForecastChart.jsx` | Animated forecast |
| `[NEW]` | `frontend2/src/widgets/Scenario/ForecastChart.css` | Styling |

### UI/UX Design Specifications

#### Visual Layout
```
┌───────────────────────────────────────────────────────────────────────┐
│  📉 Shock Trajectory & Recovery Forecast                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   $2.5M ┤                                    ╭──────────────          │
│         │     Current                       ╱    Recovery              │
│   $2.0M ┤─────────────╮                   ╱                           │
│         │              ╲                 ╱                             │
│   $1.5M ┤               ╲───────────────╯                             │
│         │                 ↑ Shock Point                                │
│   $1.0M ┤                                                              │
│         │                                                              │
│   $0.5M ┤                                                              │
│         └────┬────┬────┬────┬────┬────┬────┬────┬────┬───→            │
│             Now  +1m  +3m  +6m  +1y  +2y  +3y  +4y  +5y               │
│                                                                        │
│  Time to Break-even: 18 months │ Recovery Probability: 87%            │
└───────────────────────────────────────────────────────────────────────┘
```

#### Animation Specifications
- **Path Draw**: SVG path animates from left to right (Framer Motion, 2s duration)
- **Shock Point**: Pulsing red dot with expanding ring animation
- **Recovery Zone**: Gradient fill from red (shock) to green (recovery)
- **Tooltip Follow**: Crosshair follows cursor with value/date display
- **Confidence Band**: Shaded area showing 10th-90th percentile paths

### Verbose Acceptance Criteria

1. **Correlation Breakdown Modeling**
   - [ ] Model when all assets fall in unison (correlation → 1.0)
   - [ ] Visual indicator of "contagion risk"
   - [ ] Historical correlation during past crises
   - [ ] Dynamic correlation slider for sensitivity analysis

2. **Time-to-Break-even Calculation**
   - [ ] Based on historical recovery averages
   - [ ] Adjusts for current market conditions
   - [ ] Best/Expected/Worst case scenarios
   - [ ] Countdown display in months

3. **Multi-Scenario Comparison**
   - [ ] Zustand state saves multiple scenarios
   - [ ] Side-by-side view of up to 4 scenarios
   - [ ] Color-coded path lines per scenario
   - [ ] Export comparison report

4. **Interactive Time Scrubbing**
   - [ ] Drag slider to see portfolio value at any future point
   - [ ] Real-time probability update as time moves
   - [ ] Marker for "point of no return" if applicable

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ForecastChart.test.jsx` | Chart animates, tooltip works, scenarios compare, time scrub |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_scenario_service.py` | `test_recovery_projection`, `test_correlation_breakdown`, `test_breakeven_calculation` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 60.3: Liquidity Stress Test 'Bank Run' Simulator

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Scenario/BankRunSim.jsx` | Liquidity simulator |
| `[NEW]` | `frontend2/src/widgets/Scenario/BankRunSim.css` | Styling |

### UI/UX Design Specifications

#### Visual Layout - DOM Depletion Animation
```
┌───────────────────────────────────────────────────────────────────────┐
│  💸 Liquidity Stress Test: "Can You Exit?"                            │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Depth of Market Simulation (Your sell orders vs. available bids)     │
│                                                                        │
│  ████████████████████████████  Bid Depth                              │
│  ████████████████             Your Orders                              │
│  ██████████                   Remaining Bids After Impact             │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Position      │ Size      │ Est. Slippage │ Time to Exit │ Risk │  │
│  ├───────────────┼───────────┼───────────────┼──────────────┼──────┤  │
│  │ AAPL          │ $450,000  │ 0.12%         │ 2 min        │ 🟢   │  │
│  │ Crypto Fund LP│ $280,000  │ 3.45%         │ 72 hours     │ 🔴   │  │
│  │ Private Equity│ $150,000  │ N/A           │ 90+ days     │ ⚫   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│  Total Portfolio: $2,450,000 │ Liquid in 1 hour: $890,000 (36%)       │
│                                                                        │
│  [📋 Generate Emergency Exit Playbook]                                 │
└───────────────────────────────────────────────────────────────────────┘
```

#### Animation - DOM Depletion
- **Histogram Bars**: Animate depletion as orders consume bids (60 FPS)
- **Color Transition**: Green → Yellow → Red as depth depletes
- **Sound Effect**: Optional "cash register" sounds per lot sold
- **Completion State**: "All Clear" green banner or "Trapped" red warning

### Verbose Acceptance Criteria

1. **Depth of Market Visualization**
   - [ ] 60 FPS histogram of bid depth consumption
   - [ ] Real-time slippage calculation per position
   - [ ] Market impact preview before execution
   - [ ] Compare normal vs. crisis liquidity

2. **Toxic Position Identification**
   - [ ] Flag illiquid positions that could trap capital
   - [ ] Calculate "days to exit" for each position
   - [ ] Risk rating: 🟢 Liquid, 🟡 Moderate, 🔴 Illiquid, ⚫ Trapped
   - [ ] Suggest liquidity improvement actions

3. **Emergency Exit Playbook**
   - [ ] Auto-generate prioritized liquidation order
   - [ ] Consider tax implications in sequence
   - [ ] Broker-specific constraints (settlement, limits)
   - [ ] PDF export with SHA-256 integrity hash

4. **Scenario Parameters**
   - [ ] Adjustable market-wide liquidity factor (0.1x to 1.0x normal)
   - [ ] Time-of-day consideration (market hours vs. after-hours)
   - [ ] Concurrent seller assumptions (% of float trying to exit)

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `BankRunSim.test.jsx` | DOM animates, positions rated, playbook generates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_scenario_service.py` | `test_slippage_calculation`, `test_liquidity_rating`, `test_exit_sequence_optimization` |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/analyst/scenarios`

**Macro Task:** Black Swan Preparedness

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Scenario

# Backend
.\venv\Scripts\python.exe -m pytest tests/analysis/test_scenario_service.py -v --cov=services/analysis
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/analyst/scenarios
# Verify: Drag shock works, forecast animates, bank run simulates
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 60 with detailed UI/UX specifications |


---

# Phase 61: Philanthropy & Impact Investing Dashboard

> **Phase ID**: 61 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Completes the homeostasis loop by routing 'Excess Alpha' back to the external environment.

---

## Overview

Manages automated charitable routing and ESG impact tracking. This phase ensures that once the portfolio achieves "Enough," the excess capital is systematically directed toward positive impact, creating a sustainable equilibrium between wealth accumulation and societal benefit.

---

## Sub-Deliverable 61.1: Excess Alpha Donation Routing Interface

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Impact/DonationRouter.jsx` | Automated giving interface |
| `[NEW]` | `frontend2/src/widgets/Impact/DonationRouter.css` | Glassmorphism styling |
| `[NEW]` | `frontend2/src/stores/impactStore.js` | Impact state management |
| `[NEW]` | `services/philanthropy/donation_service.py` | Donation routing engine |
| `[NEW]` | `web/api/philanthropy_api.py` | REST endpoints |

### UI/UX Design Specifications

#### Visual Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌱 Excess Alpha Donation Router                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Your "Enough" Threshold: $3,000,000                                     │
│  Current Net Worth:       $3,247,500                                     │
│  ────────────────────────────────────────────────────────────────────   │
│  EXCESS ALPHA:            $247,500  [✨ Ready for Impact]               │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Allocation Pipeline                                             │    │
│  │                                                                   │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐                │    │
│  │  │ 🌍 Climate│───▶│ 📚 Education│──▶│ 🏥 Health│                │    │
│  │  │   40%     │    │    35%     │    │   25%    │                │    │
│  │  │ $99,000   │    │ $86,625    │    │ $61,875  │                │    │
│  │  └───────────┘    └───────────┘    └───────────┘                │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  [Configure Allocations] [Trigger Donation] [View Impact History]       │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Threshold Slider**: Drag to adjust "Enough" number (Framer Motion spring)
- **Allocation Adjustment**: Drag-and-drop percentage distribution
- **Pipeline Animation**: Flow particles move between cause categories
- **Trigger Button**: 3-second hold with progress ring to prevent accidents
- **Confirmation Modal**: Tax implication summary before execution

#### Celebration Animation
```javascript
// On successful donation
confetti({
  particleCount: 150,
  spread: 80,
  origin: { y: 0.6 },
  colors: ['#22c55e', '#3b82f6', '#f59e0b']
});
```

### Verbose Acceptance Criteria

1. **Giving API Integration**
   - [ ] GivingBlock API for crypto donations
   - [ ] CharityNavigator API for charity verification
   - [ ] Secure webhook for donation confirmation
   - [ ] Real-time status tracking

2. **Tax Deduction Alpha**
   - [ ] Calculate tax savings from charitable deductions
   - [ ] Display "Effective Cost" of donation
   - [ ] Year-end tax projection impact
   - [ ] Export for CPA documentation

3. **Impact Pulse Feed**
   - [ ] Real-time fund impact visualization
   - [ ] Projects funded by your donations
   - [ ] Beneficiary stories (where available)
   - [ ] Social sharing option (optional)

4. **Automation Rules**
   - [ ] Auto-donate when excess exceeds threshold for N days
   - [ ] Monthly/quarterly scheduled donations
   - [ ] Tax-loss harvesting coordination
   - [ ] Override controls for manual intervention

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DonationRouter.test.jsx` | Threshold slider, allocation drag, trigger hold, confirmation |
| `impactStore.test.js` | Allocation persistence, automation rules |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/philanthropy/test_donation_service.py` | `test_api_integration`, `test_tax_calculation`, `test_automation_trigger` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 61.2: ESG (Environmental, Social, Governance) Score Aggregator

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Impact/ESGScores.jsx` | Triple-gauge display |
| `[NEW]` | `frontend2/src/widgets/Impact/ESGScores.css` | Styling |
| `[NEW]` | `services/analysis/esg_service.py` | ESG data aggregation |

### UI/UX Design Specifications

#### Triple Circular Gauge Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌿 Portfolio ESG Composite Score                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│       🌎 Environmental      👥 Social          🏛️ Governance           │
│        ┌─────────┐         ┌─────────┐         ┌─────────┐              │
│        │         │         │         │         │         │              │
│        │   78    │         │   65    │         │   82    │              │
│        │   /100  │         │   /100  │         │   /100  │              │
│        └─────────┘         └─────────┘         └─────────┘              │
│           A-                   B                   A                     │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  Portfolio Karma Score: 74 / 100  ⭐⭐⭐⭐                         │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  Sin Stock Alert: 2 positions violate your filters                      │
│  [View Details] [Configure Filters]                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Gauge Animation
- **Fill Animation**: Arc fills from 0 to score value (1.5s, ease-out-cubic)
- **Color Gradient**: Red (0-30) → Yellow (31-60) → Green (61-100)
- **Hover Effect**: Gauge expands 10%, shows breakdown tooltip
- **Data Update**: Smooth transition when Kafka feeds new data

### Verbose Acceptance Criteria

1. **Real-time ESG Updates**
   - [ ] Kafka macro feeds for ESG data
   - [ ] Multiple data provider aggregation (MSCI, Sustainalytics)
   - [ ] Weighted average by position size
   - [ ] Historical trend sparklines

2. **Sin Stock Filtering**
   - [ ] User-defined "Sin Stock" categories (tobacco, arms, gambling, fossil fuels)
   - [ ] Automatic alert on exposure
   - [ ] Suggested divestment actions
   - [ ] "Ethical Exception" override with reason logging

3. **Portfolio Karma Score**
   - [ ] Aggregated ESG metric displayed in main header
   - [ ] Contribution breakdown by holding
   - [ ] Peer comparison (vs. S&P 500 ESG average)
   - [ ] Improvement recommendations

4. **Component Deep Dives**
   - [ ] Click gauge to see detailed component breakdown
   - [ ] Environmental: Carbon, Water, Waste metrics
   - [ ] Social: Labor, Diversity, Community metrics
   - [ ] Governance: Board, Ethics, Transparency metrics

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ESGScores.test.jsx` | Gauges render, animations play, sin stock alert, karma updates |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_esg_service.py` | `test_score_aggregation`, `test_sin_filter`, `test_karma_calculation` |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 61.3: Carbon Footprint vs. Portfolio Return Scatterplot

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Impact/CarbonScatter.jsx` | D3.js scatterplot |
| `[NEW]` | `frontend2/src/widgets/Impact/CarbonScatter.css` | Styling |

### UI/UX Design Specifications

#### Scatterplot Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🌡️ Alpha Efficiency vs. Carbon Intensity                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Return ▲                                                                │
│    +40% │                           ◉ NVDA                              │
│    +30% │                    ◉ MSFT      ◉ AAPL                        │
│    +20% │        ◉ NEE                                                  │
│    +10% │  ◉ AES                    ─────────── Regression Line        │
│     0%  ├──────────────────────────────────────────────────────▶       │
│   -10% │              ◉ XOM         ◉ CVX                              │
│   -20% │                        ◉ BP                                    │
│         │    Low Carbon ◀────────────────▶ High Carbon                 │
│                                                                          │
│  Correlation: -0.34 (Weak negative - ethics doesn't hurt returns)       │
│                                                                          │
│  [🌱 Offset Portfolio Carbon: $4,200]  [View Emission Details]          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns
- **Dot Sizing**: By position size (larger = bigger dot)
- **Hover Tooltip**: Company name, return, tCO2e, Scope 1/2/3 breakdown
- **Zoom/Pan**: D3 zoom behavior for exploring dense regions
- **Selection**: Click dot to highlight in portfolio grid
- **Regression Line**: Animated draw with correlation coefficient

### Verbose Acceptance Criteria

1. **Return-Efficiency Visualization**
   - [ ] Regression line showing correlation
   - [ ] Statistical significance indicator
   - [ ] Historical correlation trend
   - [ ] Sector coloring option

2. **Carbon Offset Integration**
   - [ ] One-click buy carbon credits
   - [ ] Proportional to portfolio emissions
   - [ ] Verified offset providers only
   - [ ] Certificate storage in vault

3. **Emissions Data**
   - [ ] Scope 1: Direct emissions
   - [ ] Scope 2: Electricity/energy
   - [ ] Scope 3: Value chain emissions
   - [ ] Data source attribution

4. **Portfolio Optimization**
   - [ ] "Greener Alternative" suggestions
   - [ ] Impact on expected return
   - [ ] Sector balance considerations
   - [ ] One-click swap execution

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `CarbonScatter.test.jsx` | Plot renders, hover tooltip, offset button, regression line |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/analysis/test_esg_service.py` | `test_emissions_calculation`, `test_offset_pricing`, `test_correlation_analysis` |

### Test Coverage Target: **85%**

---

## Route Integration

**Route:** `/strategist/impact`

**Macro Task:** Excess Alpha Recycling

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Impact

# Backend
.\venv\Scripts\python.exe -m pytest tests/philanthropy/ tests/analysis/test_esg_service.py -v --cov=services
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/strategist/impact
# Verify: Donation router works, ESG gauges animate, carbon scatter interactive
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 61 with enhanced UI/UX and interaction patterns |


---

# Phase 62: System Health & Hardware Telemetry Monitoring

> **Phase ID**: 62 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Prevents 'Internal Sepsis' by monitoring the physical nervous system of the AI brain.

---

## Overview

Diagnostic hub for the infrastructure supporting the autonomous swarm.

---

## Sub-Deliverable 62.1: Kafka Cluster Health & Topic Latency Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/KafkaHealth.jsx` | Cluster monitor |
| `[NEW]` | `frontend2/src/widgets/System/KafkaHealth.css` | Styling |
| `[NEW]` | `frontend2/src/stores/systemStore.js` | System state |
| `[NEW]` | `services/monitoring/kafka_health_service.py` | Kafka metrics |
| `[NEW]` | `web/api/system_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Messages Per Second**
   - [ ] Real-time scrolling bar chart per topic
   - [ ] Color-coded by topic type (Market, Signal, Risk)
   - [ ] Historical 24h comparison overlay

2. **Consumer Lag Alerts**
   - [ ] Red-alert when lag > 2,000 messages
   - [ ] Taskbar notification integration
   - [ ] Auto-scaling recommendation

3. **Restart Controls**
   - [ ] Zustand-based 'Restart Consumer' toggle
   - [ ] No full system reboot required
   - [ ] Confirmation modal with impact assessment

### Test Coverage Target: **80%**

---

## Sub-Deliverable 62.2: Database I/O & Memory Pressure Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/DBHealth.jsx` | Database monitor |
| `[NEW]` | `frontend2/src/widgets/System/DBHealth.css` | Styling |

### Verbose Acceptance Criteria

1. **Pressure Gauges**
   - [ ] Postgres WAL utilization gauge
   - [ ] Neo4j Page Cache gauge
   - [ ] Visual gradient from green to red

2. **Query Explorer**
   - [ ] Slow-query log with EXPLAIN plans
   - [ ] Cypher and SQL optimization hints
   - [ ] One-click query cancellation

3. **Disk Space Alerts**
   - [ ] Critical alert at 85% utilization
   - [ ] Automated cleanup triggers available
   - [ ] Archive old data options

### Test Coverage Target: **80%**

---

## Sub-Deliverable 62.3: Agent 'Brain' Load Balancer UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/AgentLoadBalancer.jsx` | Process viewer |
| `[NEW]` | `frontend2/src/widgets/System/AgentLoadBalancer.css` | Styling |

### Verbose Acceptance Criteria

1. **Swarm Visualization**
   - [ ] Dynamic tree of active PIDs and heartbeats
   - [ ] CPU/RAM per agent persona
   - [ ] Visual health indicators

2. **Scaling Controls**
   - [ ] One-click 'Scale Up/Down' buttons
   - [ ] Allocate more compute to StackerAgent during volatility
   - [ ] Resource limits enforcement

3. **Prometheus Integration**
   - [ ] Grafana metrics via secure proxy
   - [ ] High-fidelity telemetry charts
   - [ ] Custom dashboard embedding

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/architect/system`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 62 |


---

# Phase 63: Corporate Actions & Earnings Integrated GUI

> **Phase ID**: 63 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Tracks the fundamental 'Life Cycles' of constituents within the Yellowstone ecosystem.

---

## Overview

Interactive management of dividends, splits, and earnings cycles.

---

## Sub-Deliverable 63.1: Interactive Earnings Calendar with 'Whisper Number' Integration

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCalendar.jsx` | Calendar view |
| `[NEW]` | `frontend2/src/widgets/Corporate/EarningsCalendar.css` | Styling |
| `[NEW]` | `frontend2/src/stores/corporateStore.js` | Corporate events state |
| `[NEW]` | `services/market/earnings_service.py` | Earnings data |
| `[NEW]` | `web/api/corporate_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Implied Move Indicator**
   - [ ] Derived from current options straddle pricing
   - [ ] Visual bar showing expected range
   - [ ] Historical accuracy comparison

2. **Debate Chamber Link**
   - [ ] One-click to discuss upcoming earnings with Bull/Bear personas
   - [ ] Pre-populated context from company data
   - [ ] Trade recommendation output

3. **Portfolio Significance Filter**
   - [ ] Filter by beta-weighted exposure
   - [ ] Sector concentration impact
   - [ ] High-impact events highlighted

### Test Coverage Target: **80%**

---

## Sub-Deliverable 63.2: Dividend Reinvestment (DRIP) Management Console

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/DRIPConsole.jsx` | DRIP controls |
| `[NEW]` | `frontend2/src/widgets/Corporate/DRIPConsole.css` | Styling |

### Verbose Acceptance Criteria

1. **Yield on Cost**
   - [ ] Calculate and display per dividend payer
   - [ ] D3.js sparkline history
   - [ ] Compare to current yield

2. **Dividend Snowball**
   - [ ] 5-year projection via area charts
   - [ ] Compound growth visualization
   - [ ] "What-if" DRIP toggle comparison

3. **Income vs Expenses**
   - [ ] Annual dividend income total
   - [ ] Compare to annual expenses ("Enough" metric)
   - [ ] Gap closure projection

### Test Coverage Target: **80%**

---

## Sub-Deliverable 63.3: Stock Split & Spin-off Adjustment Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Corporate/SplitSpinoff.jsx` | Event tracker |
| `[NEW]` | `frontend2/src/widgets/Corporate/SplitSpinoff.css` | Styling |

### Verbose Acceptance Criteria

1. **Cost Basis Adjustment**
   - [ ] Auto-display adjusted cost basis
   - [ ] TimescaleDB lookup for historical data
   - [ ] Tax lot tracking

2. **Event Notifications**
   - [ ] Taskbar stream for upcoming events
   - [ ] Ticker change alerts
   - [ ] Ex-date reminders

3. **Parent/Child Visualization**
   - [ ] Neo4j relationship edges
   - [ ] Visual company family tree
   - [ ] Click to view spin-off details

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/strategist/corporate`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 63 |


---

# Phase 64: Advanced Margin & Collateral Management

> **Phase ID**: 64 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Prevents the 'Starvation' event of a margin call which leads to ecosystem collapse.

---

## Overview

Precision monitoring of buying power and liquidation risk.

---

## Sub-Deliverable 64.1: Maintenance Margin 'Danger Zone' Visualizer

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/DangerZone.jsx` | Margin gauge |
| `[NEW]` | `frontend2/src/widgets/Margin/DangerZone.css` | Styling |
| `[NEW]` | `frontend2/src/stores/marginStore.js` | Margin state |
| `[NEW]` | `services/risk/margin_service.py` | Margin calculation |
| `[NEW]` | `web/api/margin_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Distance to Liquidate**
   - [ ] Calculate % buffer for top 5 leveraged positions
   - [ ] "The Gap" metric prominently displayed
   - [ ] Real-time Kafka price feed updates

2. **Visual Warning**
   - [ ] Red pulse when margin buffer < 15%
   - [ ] Progressive urgency coloring
   - [ ] Sound alert option

3. **useRiskStore Integration**
   - [ ] Real-time collateral revaluation
   - [ ] Cross-margin calculation
   - [ ] Position-level breakdown

### Test Coverage Target: **80%**

---

## Sub-Deliverable 64.2: Cross-Collateralization Asset Priority Toggle

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/AssetPriority.jsx` | Priority list |
| `[NEW]` | `frontend2/src/widgets/Margin/AssetPriority.css` | Styling |

### Verbose Acceptance Criteria

1. **Liquidation Hierarchy**
   - [ ] Drag-and-drop priority list
   - [ ] User defines which assets sold first
   - [ ] Visual priority numbers

2. **Impact Calculator**
   - [ ] Real-time margin impact of selling each asset
   - [ ] Cascade effect visualization
   - [ ] Optimal sequence suggestion

3. **Protected Assets**
   - [ ] Mark core holdings as "Protected"
   - [ ] Agents barred from touching
   - [ ] Visual shield icon

### Test Coverage Target: **80%**

---

## Sub-Deliverable 64.3: Automated Margin Call Liquidation Order Editor

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Margin/GhostOrderViewer.jsx` | Broker preview |
| `[NEW]` | `frontend2/src/widgets/Margin/GhostOrderViewer.css` | Styling |

### Verbose Acceptance Criteria

1. **Worst Case Preview**
   - [ ] Visualize broker's auto-liquidation orders
   - [ ] Expected slippage calculation
   - [ ] Order book sweep simulation

2. **One-Click De-leverage**
   - [ ] Restore 20% margin safety buffer
   - [ ] Optimal position sizing
   - [ ] Confirmation with impact summary

3. **Audit Logging**
   - [ ] Every margin-check event logged
   - [ ] Risk governor trigger history
   - [ ] Regulatory compliance trail

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/guardian/margin`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 64 |


---

# Phase 65: Mobile Portfolio Quick-Actions (V2)

> **Phase ID**: 65 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Empowers the 'Warden' with remote intervention capabilities from anywhere on Earth.

---

## Overview

Advanced mobile features for system oversight and emergency control.

---

## Sub-Deliverable 65.1: Biometric 'Kill Switch' for Android/iOS

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Mobile/KillSwitch.jsx` | Emergency button |
| `[NEW]` | `frontend2/src/widgets/Mobile/KillSwitch.css` | Styling |
| `[NEW]` | `services/emergency/mobile_kill_service.py` | Mobile integration |

### Verbose Acceptance Criteria

1. **Long Press Activation**
   - [ ] 3-second hold requirement
   - [ ] Haptic feedback intensity 1.0
   - [ ] Visual progress ring
   - [ ] Prevent accidental trigger

2. **Kafka Broadcast**
   - [ ] Immediate `emergency-kill` topic publish
   - [ ] < 100ms latency target
   - [ ] Confirmation receipt

3. **Desktop Sync**
   - [ ] Push notification to all linked instances
   - [ ] State synchronization
   - [ ] Audit trail entry

### Test Coverage Target: **80%**

---

## Sub-Deliverable 65.2: Push-Notification Trade Authorization (OAuth 2.0)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Mobile/TradeAuth.jsx` | Authorization flow |
| `[NEW]` | `frontend2/src/widgets/Mobile/TradeAuth.css` | Styling |

### Verbose Acceptance Criteria

1. **Deep-Link Logic Summary**
   - [ ] Link to LLM Debate summary before approval
   - [ ] Trade rationale displayed
   - [ ] Risk assessment included

2. **Biometric Signature**
   - [ ] Required for trades > $10,000
   - [ ] OAuth 2.0 secure flow
   - [ ] Session expiry handling

3. **Time-Limited Approval**
   - [ ] 60-second window before auto-cancel
   - [ ] Visual countdown timer
   - [ ] Extension request option

### Test Coverage Target: **80%**

---

## Sub-Deliverable 65.3: Haptic-Feedback Real-time Alert Vibrations

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Mobile/HapticAlerts.jsx` | Vibration config |
| `[NEW]` | `frontend2/src/widgets/Mobile/HapticAlerts.css` | Styling |

### Verbose Acceptance Criteria

1. **Pattern Differentiation**
   - [ ] Single sharp pulse for 'Info'
   - [ ] Long heavy vibration for 'Critical'
   - [ ] Pattern library with previews

2. **Dynamic Intensity**
   - [ ] Frequency increases with Fear Index
   - [ ] Margin Danger level correlation
   - [ ] User sensitivity settings

3. **Quiet Hours**
   - [ ] Configurable quiet periods
   - [ ] Mandatory override for Black Swan events
   - [ ] Do Not Disturb integration

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/mobile/settings`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 65 |


---

# Phase 66: API Marketplace & Integration Manager

> **Phase ID**: 66 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Allows the ecosystem to ingest 'New Senses' and adapt to changing market landscapes.

---

## Overview

Hub for connecting third-party data providers and external webhooks.

---

## Sub-Deliverable 66.1: Third-party Data Connector (Alpha Vantage, Polygon, FRED)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/DataConnector.jsx` | Provider manager |
| `[NEW]` | `frontend2/src/widgets/API/DataConnector.css` | Styling |
| `[NEW]` | `frontend2/src/stores/apiStore.js` | API state |
| `[NEW]` | `services/integration/api_connector_service.py` | Connector logic |
| `[NEW]` | `web/api/integration_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Real-time Ping Status**
   - [ ] Sub-second health polling per provider
   - [ ] Green/Yellow/Red status indicators
   - [ ] Latency measurement display

2. **Rate Limit Gauges**
   - [ ] Visual utilization bars
   - [ ] Prevent data-tap "Starvation"
   - [ ] Quota reset countdown

3. **Automatic Failover**
   - [ ] Toggle for secondary provider failover
   - [ ] Seamless data continuity
   - [ ] Failover event logging

### Test Coverage Target: **80%**

---

## Sub-Deliverable 66.2: API Key Encryption/Vaulting UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/KeyVault.jsx` | Key management |
| `[NEW]` | `frontend2/src/widgets/API/KeyVault.css` | Styling |

### Verbose Acceptance Criteria

1. **Masked Display**
   - [ ] Keys hidden by default (•••••)
   - [ ] Biometric re-auth to reveal
   - [ ] Copy-to-clipboard with auto-clear

2. **Audit Trail**
   - [ ] Track which agent/user accessed vault
   - [ ] Timestamp and action logging
   - [ ] Anomaly detection alerts

3. **HashiCorp Vault Integration**
   - [ ] Secure backend credential isolation
   - [ ] Secret rotation support
   - [ ] Lease management

### Test Coverage Target: **80%**

---

## Sub-Deliverable 66.3: Custom Webhook Trigger Configuration

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/API/WebhookBuilder.jsx` | Webhook config |
| `[NEW]` | `frontend2/src/widgets/API/WebhookBuilder.css` | Styling |

### Verbose Acceptance Criteria

1. **Payload Builder**
   - [ ] Visual template editor
   - [ ] Liquid template support
   - [ ] Dynamic JSON data insertion

2. **Test Functionality**
   - [ ] 'Send Test' button
   - [ ] Real-time response log
   - [ ] Status code display

3. **Filtering Options**
   - [ ] Filter by alert severity
   - [ ] Filter by Kafka topic
   - [ ] Filter by agent persona

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/architect/api`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 66 |


---

# Phase 67: Real-Estate & Illiquid Asset Tracking

> **Phase ID**: 67 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Incorporates 'Slow Capital' into the high-frequency Net Worth model for total wealth homeostasis.

---

## Overview

Tracking of physical assets, private equity, and manual entries.

---

## Sub-Deliverable 67.1: Manual Asset Entry (Physical Property, Art, Private Equity)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/ManualEntry.jsx` | Entry forms |
| `[NEW]` | `frontend2/src/widgets/Assets/ManualEntry.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Assets/AssetCategories.jsx` | Category picker |
| `[NEW]` | `frontend2/src/stores/wealthStore.js` | Wealth state |
| `[NEW]` | `services/portfolio/assets_service.py` | Asset persistence |
| `[NEW]` | `web/api/assets_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Neo4j Entity Linking**
   - [ ] Link to `ENTITY` nodes for jurisdictional mapping
   - [ ] Tax implications per entity type
   - [ ] Ownership percentage tracking

2. **Document Upload**
   - [ ] Appraisals and insurance uploads
   - [ ] Vault integration with "Missing Document" warnings
   - [ ] Expiration tracking

3. **TotalWealth Merge**
   - [ ] Single Zustand slice for liquid + illiquid
   - [ ] Combined Net Worth calculation
   - [ ] View toggle: Liquid/Illiquid/All

4. **Category Support**
   - [ ] Real Estate (Primary, Rental, Vacation)
   - [ ] Art & Collectibles
   - [ ] Private Equity/Venture
   - [ ] Vehicles & Personal Property

### Test Coverage Target: **80%**

---

## Sub-Deliverable 67.2: Estimated Valuation Depreciation/Appreciation Slider

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/ValuationSlider.jsx` | Value adjuster |
| `[NEW]` | `frontend2/src/widgets/Assets/ValuationSlider.css` | Styling |

### Verbose Acceptance Criteria

1. **Real-time Impact**
   - [ ] D3.js gauges update as slider moves
   - [ ] Delta display: "+$50,000 (↑2.1%)"
   - [ ] Save/Undo functionality

2. **API Integration**
   - [ ] Zillow/Redfin property estimates
   - [ ] "Zestimate" comparison
   - [ ] Auto-update toggle

3. **Historical Timeline**
   - [ ] TimescaleDB storage
   - [ ] Value chart over time
   - [ ] Inflation comparison

### Test Coverage Target: **80%**

---

## Sub-Deliverable 67.3: Unified Wealth 'Net Worth' Circular Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Assets/NetWorthGauges.jsx` | D3.js visualization |
| `[NEW]` | `frontend2/src/widgets/Assets/NetWorthGauges.css` | Styling |

### Verbose Acceptance Criteria

1. **Dual-Ring Design**
   - [ ] Inner ring: Liquid (Stocks/Crypto/Cash)
   - [ ] Outer ring: Illiquid (Real Estate/PE/Art)
   - [ ] Color-coded segments

2. **Center Display**
   - [ ] Total Net Worth prominently shown
   - [ ] 24h change with delta
   - [ ] "All-Time High" badge

3. **Framer Motion Animation**
   - [ ] 60 FPS ring animation on load
   - [ ] Smooth segment transitions
   - [ ] Hover expansion for details

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/assets`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 67 |


---

# Phase 68: The Homeostasis 'Zen' Mode

> **Phase ID**: 68 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: The ultimate goal: the absence of unnecessary oscillation and the focus on 'Enough'.

---

## Overview

A minimalist interface focused on long-term peace of mind and goal achievement. This is the terminal phase of the AI_Investor expansion, representing the pinnacle of the homeostasis philosophy.

---

## Sub-Deliverable 68.1: Minimalist Goal Tracking UI (The 'Enough' Metric)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/pages/ZenMode.jsx` | Zen page |
| `[NEW]` | `frontend2/src/widgets/Zen/ZenMode.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Zen/GoalProgress.jsx` | Progress bar |
| `[NEW]` | `services/portfolio/homeostasis_service.py` | Zen logic |

### Verbose Acceptance Criteria

1. **Noise Reduction**
   - [ ] Hide all price charts
   - [ ] No red/green flash indicators
   - [ ] Calm, muted color palette
   - [ ] Slow, deliberate animations only

2. **Freedom Number Progress**
   - [ ] Simple progress bar to user-defined "Freedom Number"
   - [ ] Tailwind neon "Glow" effect when goal reached
   - [ ] Percentage complete display
   - [ ] "You're X% to Enough" message

3. **Income vs Expenses Focus**
   - [ ] "Projected Annual Income" from dividends/interest
   - [ ] vs "Annual Expenses" (user-defined)
   - [ ] "Covered: X years of expenses" calculation
   - [ ] "The Gap" metric for homeostasis

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.2: Time-to-Retirement Countdown & Probability Gauge

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Zen/RetirementGauge.jsx` | D3.js gauge |
| `[NEW]` | `frontend2/src/widgets/Zen/RetirementGauge.css` | Styling |

### Verbose Acceptance Criteria

1. **Monte Carlo Survival**
   - [ ] 10k path simulation
   - [ ] Target > 99% success probability
   - [ ] Red warning if < 90%
   - [ ] Animated probability display

2. **Safety Buffer**
   - [ ] "X years of expenses covered" display
   - [ ] Adjust for inflation
   - [ ] Best/Expected/Worst scenarios
   - [ ] Visual confidence band

3. **Lifestyle Toggle**
   - [ ] Zustand-based "Frugal vs Lux" switch
   - [ ] Immediate recalculation
   - [ ] Side-by-side comparison option

### Test Coverage Target: **80%**

---

## Sub-Deliverable 68.3: System Autopilot Master Override (The 'Peace of Mind' Toggle)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Zen/AutopilotToggle.jsx` | Master switch |
| `[NEW]` | `frontend2/src/widgets/Zen/AutopilotToggle.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/Zen/HomeostasisOverlay.jsx` | Zen overlay |

### Verbose Acceptance Criteria

1. **High-Frequency Disable**
   - [ ] Disable all high-frequency Kafka consumers
   - [ ] Agents shift to dividend-seeking logic
   - [ ] No active trading mode
   - [ ] Capital preservation focus

2. **Manual Trading Lock**
   - [ ] Lock out all manual trading buttons
   - [ ] Prevent emotional intervention
   - [ ] Re-authentication required to unlock
   - [ ] Cool-down period enforcement

3. **Homeostatic Display**
   - [ ] "System Homeostatic" status message
   - [ ] 20px backdrop-blur overlay
   - [ ] Slow-moving particle animation
   - [ ] Optional calming ambient sounds

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/zen`

**Macro Task:** Ultimate Equilibrium

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Zen

# Backend
.\venv\Scripts\python.exe -m pytest tests/portfolio/test_homeostasis_service.py -v --cov=services/portfolio
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/zen
# Verify: Goal progress shown, no flashy charts, autopilot toggles correctly
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 68 - Final Phase |


---

# UI Phase X2 Roadmap (Phases 49–68)

> **Strategic Goal**: Transition from a tactical Trading Terminal to a **Total Financial Homeostasis Engine** using the *Yellowstone Wolf Principle*.

---

## Phase Overview

| Phase | Title | Strategic Purpose |
|-------|-------|-------------------|
| 49 | Advanced Portfolio Attribution | Accountability layer (Alpha vs Beta) |
| 50 | Fixed Income & Yield Curve | Interest rate "Climate" monitoring |
| 51 | Web3 Vaulting & DeFi GUI | Decentralized metabolism integration |
| 52 | Tax-Advantaged Harvesting | Dead capital recycling |
| 53 | Global Macro & Commodities | Environmental condition foresight |
| 54 | Institutional KYC & Vault | Fort Knox legal boundary |
| 55 | Debate Chamber 2.0 | Swarm logic exposure |
| 56 | Multi-Currency Cash Mgmt | Global liquidity pulse |
| 57 | Backtest Explorer V2 | Monte Carlo robustness |
| 58 | Estate Planning Wizard | Ecosystem life extension |
| 59 | Regulatory Compliance | Lawful predator assurance |
| 60 | Scenario 'What-If' Simulator | Black swan stress testing |
| 61 | Philanthropy & Impact | Excess alpha routing |
| 62 | System Health Telemetry | Internal sepsis prevention |
| 63 | Corporate Actions & Earnings | Constituent life cycles |
| 64 | Margin & Collateral Mgmt | Starvation event prevention |
| 65 | Mobile Quick-Actions V2 | Remote warden intervention |
| 66 | API Marketplace | New senses ingestion |
| 67 | Real-Estate & Illiquid | Slow capital integration |
| 68 | Homeostasis 'Zen' Mode | Ultimate equilibrium state |

---

## Implementation Waves

### Wave 1: Foundation & Accountability (Phases 49–52)
- [/] Phase 49: Brinson-Fachler Attribution UI
- [ ] Phase 50: Bond Ladder & Yield Curve
- [ ] Phase 51: Hardware Wallet & LP Tracker
- [ ] Phase 52: Tax-Loss Harvesting UI

### Wave 2: Macro Intelligence (Phases 53–56)
- [ ] Phase 53: World Map & Futures Curves
- [ ] Phase 54: KYC Portal & Document Vault
- [ ] Phase 55: Multi-Agent Debate Interface
- [ ] Phase 56: FX Management & Cash Pulse

### Wave 3: Robustness & Compliance (Phases 57–60)
- [ ] Phase 57: Monte Carlo Path Visualizer
- [ ] Phase 58: Dead Man's Switch & Estate
- [ ] Phase 59: Audit Log & SAR Workflow
- [ ] Phase 60: Macro Shock Simulator

### Wave 4: Impact & Infrastructure (Phases 61–64)
- [ ] Phase 61: ESG Aggregator & Donation Routing
- [ ] Phase 62: Kafka/Postgres/Neo4j Health
- [ ] Phase 63: Earnings Calendar & DRIP
- [ ] Phase 64: Margin Danger & Liquidation

### Wave 5: Mobility & Integration (Phases 65–68)
- [ ] Phase 65: Biometric Kill Switch (Mobile)
- [ ] Phase 66: API Connector & Webhook Builder
- [ ] Phase 67: Illiquid Asset Entry & Valuation
- [ ] Phase 68: Zen Mode & Autopilot Override

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| Frontend | React 19 & Vite |
| State | Zustand (multi-slice) |
| Event Bus | Kafka (Redpanda) |
| Graph DB | Neo4j |
| Time Series | Postgres (TimescaleDB) |
| Visuals | D3.js & HTML5 Canvas |
| Animation | Framer Motion |

---

## Design Philosophy

- **Glassmorphism HUD**: 20px `backdrop-filter: blur()` with 70% opacity
- **7:1 Contrast Ratio**: Professional readability
- **60 FPS Target**: All visualizations and animations
- **Cognitive Decoupling**: Reduce noise, focus on "Enough" metric

---

## Key Deliverables Per Phase

### Phase 49: Attribution
1. Sector Allocation Widget (D3.js)
2. Interaction Effect Heatmap
3. Benchmark Relative-Strength Overlay

### Phase 50: Fixed Income
1. Bond Ladder Constructor
2. FRED API Yield Curve Plotter
3. Duration/Convexity Gauges

### Phase 51: Web3
1. Hardware Wallet Dashboard
2. LP Position Tracker (IL calc)
3. Gas Fee Optimizer

### Phase 52: Tax
1. Wash-Sale Protected Grid
2. Automated Harvesting Toggle
3. Capital Gains Forecaster

### Phase 53: Macro
1. D3 World Map (Shipping + Politics)
2. Contango/Backwardation Visualizer
3. Inflation Correlation Matrix

### Phase 54: KYC
1. Encrypted ID Verification Portal
2. Audit-Trail Document System
3. 13F Filing Tracker

### Phase 55: Debate
1. Bull vs Bear Chat Interface
2. Voting Consensus Bar
3. Argument Tree (Neo4j)

### Phase 56: FX
1. Global Cash Pulse Widget
2. Limit-Order FX Interface
3. Cash Optimization Dashboard

### Phase 57: Backtest
1. Monte Carlo 10k Paths (Canvas)
2. Max Drawdown Timeline
3. Out-of-Sample Variance Matrix

### Phase 58: Estate
1. Dead Man's Switch Config
2. Beneficiary Allocation Tree
3. Trust/Entity Visualizer (Neo4j)

### Phase 59: Compliance
1. Anti-Market Abuse Feed
2. Immutable Audit Log (SHA-256)
3. SAR Flagging UI

### Phase 60: Scenarios
1. Macro Event Drag-Drop Trigger
2. Shock Trajectory Chart
3. Bank Run Simulator

### Phase 61: Philanthropy
1. Excess Alpha Donation Router
2. ESG Score Aggregator
3. Carbon Footprint Scatterplot

### Phase 62: System Health
1. Kafka Cluster Dashboard
2. DB I/O Gauges
3. Agent Load Balancer

### Phase 63: Corporate Actions
1. Earnings Calendar (Whisper #)
2. DRIP Management Console
3. Split/Spin-off Visualizer

### Phase 64: Margin
1. Danger Zone Visualizer
2. Cross-Collateral Priority Toggle
3. Automated Liquidation Editor

### Phase 65: Mobile V2
1. Biometric Kill Switch
2. Push Trade Authorization
3. Haptic Alert Patterns

### Phase 66: API Hub
1. Data Connector UI
2. API Key Vault
3. Webhook Trigger Builder

### Phase 67: Illiquid
1. Manual Asset Entry Forms
2. Appreciation/Depreciation Slider
3. Unified Net Worth Gauges

### Phase 68: Zen Mode
1. "Enough" Metric Progress Bar
2. Retirement Countdown Gauge
3. Autopilot Master Override

---

## Success Metrics

1. **Systemic Evolution**: Tactical → Macro-governance engine
2. **Cognitive Load Reduction**: Noise elimination via "Enough" metric
3. **Institutional Durability**: Legal + inheritance protocols
4. **60 FPS Visuals**: All D3/Canvas renderings
5. **Sub-100ms Latency**: All Zustand state updates


---

