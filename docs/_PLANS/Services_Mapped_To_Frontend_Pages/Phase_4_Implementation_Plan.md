# Phase 4 Implementation Plan: Market Data Foundation

> **Phase**: 4 of 33  
> **Status**: 🔴 Not Started  
> **Priority**: HIGH  
> **Estimated Duration**: 5 days  
> **Dependencies**: Phase 1 (Infrastructure)

---

## Overview

Phase 4 establishes the market data visualization layer, including forced seller detection, whale flow tracking, volume promo detection, technical indicators, and market regime classification.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `market_data` | `services/market_data/` | `forced_seller_svc.py`, `fund_flow_service.py`, `volume_monitor.py` |
| `market` | `services/market/` | `regime_classifier.py`, `price_service.py` |
| `data` | `services/data/` | `data_manager.py`, `time_series.py` |
| `indicators` | `services/indicators/` | `indicator_engine.py`, `custom_indicators.py` |

---

## Deliverable 1: Forced Seller Monitor Page

### 1.1 Description
Full-page interface (`/data-scientist/forced-sellers`) analyzing passive ownership concentration and structural fragility risks.

### 1.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `ForcedSellerMonitor.jsx` | `frontend/src/pages/data-scientist/ForcedSellerMonitor.jsx` | Page |
| `PassiveConcentrationHeatmap.jsx` | `frontend/src/components/charts/PassiveConcentrationHeatmap.jsx` | Chart |
| `FragilityScoreCard.jsx` | `frontend/src/components/cards/FragilityScoreCard.jsx` | Card |
| `LiquidityTrapAlert.jsx` | `frontend/src/components/alerts/LiquidityTrapAlert.jsx` | Alert |
| `SectorFragilityTable.jsx` | `frontend/src/components/tables/SectorFragilityTable.jsx` | Table |

### 1.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/market-data/forced-sellers` | `list_forced_seller_risks()` |
| GET | `/api/v1/market-data/forced-sellers/{ticker}` | `get_ticker_fragility()` |
| GET | `/api/v1/market-data/forced-sellers/heatmap` | `get_passive_heatmap()` |
| GET | `/api/v1/market-data/forced-sellers/sectors` | `get_sector_fragility()` |
| GET | `/api/v1/market-data/liquidity-traps` | `get_active_traps()` |

### 1.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F4.1.1**: Heatmap shows passive ownership % by sector/ticker
- [ ] **F4.1.2**: Fragility score (0-100) calculated per ticker with risk level
- [ ] **F4.1.3**: Liquidity trap alerts when bid-ask spread expands >2.5x
- [ ] **F4.1.4**: Sector table shows aggregate sector fragility scores
- [ ] **F4.1.5**: Click ticker to drill into detailed ownership breakdown

#### Integration Requirements
- [ ] **I4.1.1**: Heatmap data fetched from `/api/v1/market-data/forced-sellers/heatmap`
- [ ] **I4.1.2**: Real-time alerts via WebSocket subscription
- [ ] **I4.1.3**: Historical fragility trend available for each ticker
- [ ] **I4.1.4**: Data refreshed every 5 minutes during market hours

#### Response Handling
- [ ] **R4.1.1**: Fragility schema: `{ ticker, passive_pct, fragility_score, risk_level, last_updated }`
- [ ] **R4.1.2**: Trap alert schema: `{ ticker, spread_expansion, timestamp, severity }`
- [ ] **R4.1.3**: 503 when market data provider unavailable

---

## Deliverable 2: Whale Flow Terminal Page

### 2.1 Description
Page (`/data-scientist/whale-flow`) visualizing institutional 13F filing deltas, whale selling pressure, and sector overcrowding.

### 2.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `WhaleFlowTerminal.jsx` | `frontend/src/pages/data-scientist/WhaleFlowTerminal.jsx` | Page |
| `FilingDeltaTimeline.jsx` | `frontend/src/components/charts/FilingDeltaTimeline.jsx` | Chart |
| `WhaleSellingTable.jsx` | `frontend/src/components/tables/WhaleSellingTable.jsx` | Table |
| `SectorCrowdingGauge.jsx` | `frontend/src/components/charts/SectorCrowdingGauge.jsx` | Chart |
| `InstitutionalHolderCard.jsx` | `frontend/src/components/cards/InstitutionalHolderCard.jsx` | Card |

### 2.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/market-data/whale-flow` | `get_whale_flow_summary()` |
| GET | `/api/v1/market-data/whale-flow/{ticker}` | `get_ticker_whale_activity()` |
| GET | `/api/v1/market-data/whale-flow/filings` | `get_recent_filings()` |
| GET | `/api/v1/market-data/whale-flow/crowding` | `get_sector_crowding()` |
| GET | `/api/v1/market-data/whale-flow/holders/{holder_id}` | `get_holder_details()` |

### 2.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F4.2.1**: Timeline shows 13F filing dates with position change magnitude
- [ ] **F4.2.2**: Table lists top sellers with shares sold, % change, holder name
- [ ] **F4.2.3**: Sector crowding gauge (0-100) with overcrowding threshold (80)
- [ ] **F4.2.4**: Holder card shows portfolio composition and recent changes
- [ ] **F4.2.5**: Filter by date range, holder type, minimum change size

#### Integration Requirements
- [ ] **I4.2.1**: Filing data parsed from SEC EDGAR 13F files
- [ ] **I4.2.2**: Crowding scores recalculated daily at market close
- [ ] **I4.2.3**: Holder details link to SEC filing source
- [ ] **I4.2.4**: Pagination for large filing result sets

#### Response Handling
- [ ] **R4.2.1**: Whale activity schema: `{ ticker, holders: [{ name, change_shares, change_pct }] }`
- [ ] **R4.2.2**: Crowding schema: `{ sector, crowding_score, top_crowded_tickers[] }`
- [ ] **R4.2.3**: Filing parse errors logged; partial data returned

---

## Deliverable 3: Volume Promo Detector Widget

### 3.1 Description
Widget embedded in Market Intelligence showing volume spike detection correlated with social media sentiment.

### 3.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `VolumePromoWidget.jsx` | `frontend/src/components/widgets/VolumePromoWidget.jsx` | Widget |
| `VolumeSpikeBadge.jsx` | `frontend/src/components/badges/VolumeSpikeBadge.jsx` | Badge |
| `SentimentVolumeChart.jsx` | `frontend/src/components/charts/SentimentVolumeChart.jsx` | Chart |
| `PromoAlertCard.jsx` | `frontend/src/components/cards/PromoAlertCard.jsx` | Card |

### 3.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/market-data/promo-spikes` | `get_promo_spikes()` |
| GET | `/api/v1/market-data/promo-spikes/{ticker}` | `get_ticker_promo_history()` |
| GET | `/api/v1/market-data/volume/baseline/{ticker}` | `get_volume_baseline()` |
| WS | `/ws/market-data/promo-alerts` | `stream_promo_alerts()` |

### 3.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F4.3.1**: Widget shows active promo spike tickers with severity
- [ ] **F4.3.2**: Chart overlays volume with social sentiment score
- [ ] **F4.3.3**: Badge shows "PROMO SPIKE" when conditions met
- [ ] **F4.3.4**: Historical promo events timeline per ticker
- [ ] **F4.3.5**: Real-time alerts for new promo spike detection

#### Integration Requirements
- [ ] **I4.3.1**: Promo detection triggers when volume >2x average AND sentiment >0.9
- [ ] **I4.3.2**: Baseline uses 4-week moving average volume
- [ ] **I4.3.3**: WebSocket pushes new alerts immediately
- [ ] **I4.3.4**: Social sentiment aggregated from StockTwits, Reddit

#### Response Handling
- [ ] **R4.3.1**: Spike schema: `{ ticker, volume_ratio, sentiment_score, is_promo, action }`
- [ ] **R4.3.2**: Alert schema: `{ ticker, detected_at, severity, recommended_action }`
- [ ] **R4.3.3**: Social data unavailable shows "Partial data" warning

---

## Deliverable 4: Technical Indicators Page

### 4.1 Description
Full-page interface (`/data-scientist/indicators`) providing a complete indicator library with parameter tuning and custom indicator creation.

### 4.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `TechnicalIndicatorsPage.jsx` | `frontend/src/pages/data-scientist/TechnicalIndicatorsPage.jsx` | Page |
| `IndicatorLibrary.jsx` | `frontend/src/components/data-scientist/IndicatorLibrary.jsx` | Widget |
| `IndicatorChart.jsx` | `frontend/src/components/charts/IndicatorChart.jsx` | Chart |
| `ParameterTuner.jsx` | `frontend/src/components/forms/ParameterTuner.jsx` | Form |
| `CustomIndicatorEditor.jsx` | `frontend/src/components/editors/CustomIndicatorEditor.jsx` | Editor |

### 4.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/indicators` | `list_indicators()` |
| GET | `/api/v1/indicators/{indicator_id}` | `get_indicator_details()` |
| POST | `/api/v1/indicators/calculate` | `calculate_indicator()` |
| POST | `/api/v1/indicators/custom` | `create_custom_indicator()` |
| GET | `/api/v1/indicators/custom` | `list_custom_indicators()` |

### 4.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F4.4.1**: Library lists 50+ built-in indicators (SMA, EMA, RSI, MACD, etc.)
- [ ] **F4.4.2**: Parameter tuner allows adjusting indicator settings
- [ ] **F4.4.3**: Chart shows indicator output overlaid on price data
- [ ] **F4.4.4**: Custom indicator editor supports Python-like syntax
- [ ] **F4.4.5**: Save/load indicator presets per user

#### Integration Requirements
- [ ] **I4.4.1**: Calculate POST includes `{ ticker, indicator, params, period }`
- [ ] **I4.4.2**: Custom indicators validated before save
- [ ] **I4.4.3**: Indicator calculation uses streaming price data
- [ ] **I4.4.4**: Results cached for 1 minute per calculation

#### Response Handling
- [ ] **R4.4.1**: Indicator list schema: `[{ id, name, category, params[] }]`
- [ ] **R4.4.2**: Calculate result: `{ indicator, values: [{ timestamp, value }] }`
- [ ] **R4.4.3**: Custom indicator syntax errors return line/column

---

## Deliverable 5: Market Regime Classifier Widget

### 5.1 Description
Widget for Strategist Dashboard showing current market regime (Bull/Bear/Choppy) with confidence score and historical regime timeline.

### 5.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `MarketRegimeWidget.jsx` | `frontend/src/components/widgets/MarketRegimeWidget.jsx` | Widget |
| `RegimeIndicator.jsx` | `frontend/src/components/indicators/RegimeIndicator.jsx` | Indicator |
| `RegimeTimeline.jsx` | `frontend/src/components/charts/RegimeTimeline.jsx` | Chart |
| `RegimeBreakdownCard.jsx` | `frontend/src/components/cards/RegimeBreakdownCard.jsx` | Card |

### 5.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/market/regime` | `get_current_regime()` |
| GET | `/api/v1/market/regime/history` | `get_regime_history()` |
| GET | `/api/v1/market/regime/indicators` | `get_regime_indicators()` |
| GET | `/api/v1/market/regime/forecast` | `get_regime_forecast()` |

### 5.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F4.5.1**: Widget displays current regime (BULL/BEAR/CHOPPY/TRANSITION)
- [ ] **F4.5.2**: Confidence score (0-100%) for current classification
- [ ] **F4.5.3**: Timeline shows regime changes over selected period
- [ ] **F4.5.4**: Breakdown shows contributing indicators with weights
- [ ] **F4.5.5**: Forecast shows predicted regime for next 5/10/20 days

#### Integration Requirements
- [ ] **I4.5.1**: Regime calculated from VIX, trend, breadth, momentum
- [ ] **I4.5.2**: Updated every 15 minutes during market hours
- [ ] **I4.5.3**: Historical data available for 2 years
- [ ] **I4.5.4**: Color coding: green (Bull), red (Bear), yellow (Choppy)

#### Response Handling
- [ ] **R4.5.1**: Regime schema: `{ regime, confidence, since, indicators[] }`
- [ ] **R4.5.2**: History schema: `[{ date, regime, duration_days }]`
- [ ] **R4.5.3**: Forecast schema: `{ forecast_regime, probability, as_of }`

---

## Testing Requirements

### Unit Tests
| Component | Test File | Coverage Target |
|-----------|-----------|-----------------|
| ForcedSellerMonitor | `tests/frontend/data-scientist/ForcedSellerMonitor.test.jsx` | 80% |
| WhaleFlowTerminal | `tests/frontend/data-scientist/WhaleFlowTerminal.test.jsx` | 80% |
| market_data_api | `tests/backend/api/test_market_data_api.py` | 90% |
| indicator_api | `tests/backend/api/test_indicator_api.py` | 90% |

### Integration Tests
| Test Suite | Description |
|------------|-------------|
| `test_phase4_forced_seller_e2e.py` | Heatmap load → ticker drill-down → trap alert |
| `test_phase4_whale_flow_e2e.py` | Timeline → holder details → crowding gauge |
| `test_phase4_indicators_e2e.py` | Select indicator → tune params → calculate |
| `test_phase4_regime_e2e.py` | Widget load → history timeline → forecast |

---

## Deployment Checklist

- [ ] Market data provider API keys configured
- [ ] 13F filing parser scheduled
- [ ] Social sentiment aggregator connected
- [ ] Indicator library populated
- [ ] Regime classifier model deployed
- [ ] Real-time WebSocket handlers registered
- [ ] Frontend routes and navigation updated
- [ ] Documentation complete

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 4 Implementation Plan - Version 1.0*
