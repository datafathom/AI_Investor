# Phase 8 Implementation Plan: Charting & Visualization

> **Phase**: 8 of 33 | **Status**: 🔴 Not Started | **Priority**: HIGH  
> **Duration**: 5 days | **Dependencies**: Phase 4

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `charting` | `chart_engine.py`, `mtf_analyzer.py`, `heatmap_generator.py` |
| `pricing` | `probability_cone.py`, `expected_move.py` |

---

## Deliverable 1: Advanced Chart Builder

### Frontend: `AdvancedChartBuilder.jsx`, `ChartCanvas.jsx`, `DrawingToolbar.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/charting/candles/{ticker}` | `get_candle_data()` |
| POST | `/api/v1/charting/indicators/calculate` | `calculate_indicator()` |
| POST | `/api/v1/charting/drawings/{chart_id}` | `save_drawings()` |

### Acceptance Criteria
- [ ] **F8.1.1**: Interactive candlestick with zoom, pan, crosshair
- [ ] **F8.1.2**: 50+ indicators (MA, RSI, MACD, Bollinger)
- [ ] **F8.1.3**: Drawing tools: trendlines, Fibonacci, channels
- [ ] **F8.1.4**: Timeframes: 1m to 1M
- [ ] **F8.1.5**: Save/load chart layouts

---

## Deliverable 2: Multi-Timeframe Analysis Widget

### Frontend: `MultiTimeframeWidget.jsx`, `SyncedChartGrid.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/charting/mtf/{ticker}` | `get_mtf_data()` |
| GET | `/api/v1/charting/mtf/{ticker}/signals` | `get_mtf_signals()` |

### Acceptance Criteria
- [ ] **F8.2.1**: 2x2 or 3x1 synchronized chart grid
- [ ] **F8.2.2**: Crosshair syncs across timeframes
- [ ] **F8.2.3**: MTF alignment signal (bullish/bearish/mixed)

---

## Deliverable 3: Options Probability Cone Widget

### Frontend: `ProbabilityConeWidget.jsx`, `ConeChart.jsx`, `ExpectedMoveCard.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/pricing/probability-cone/{ticker}` | `get_probability_cone()` |
| GET | `/api/v1/pricing/expected-move/{ticker}` | `get_expected_move()` |

### Acceptance Criteria
- [ ] **F8.3.1**: Cone shows 1σ, 2σ bands over time
- [ ] **F8.3.2**: Expected move ± range for expiration
- [ ] **F8.3.3**: Probability table for price levels

---

## Deliverable 4: Heatmap Generator Page

### Frontend: `HeatmapGenerator.jsx`, `HeatmapCanvas.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/charting/heatmaps/correlation` | `get_correlation_heatmap()` |
| GET | `/api/v1/charting/heatmaps/sector` | `get_sector_heatmap()` |

### Acceptance Criteria
- [ ] **F8.4.1**: Correlation heatmap for portfolio
- [ ] **F8.4.2**: Sector performance heatmap
- [ ] **F8.4.3**: Export as PNG/SVG

---

## Deliverable 5: Chart Export & Sharing

### Frontend: `ChartExportModal.jsx`, `ShareLinkGenerator.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/charting/export` | `export_chart()` |
| POST | `/api/v1/charting/share` | `create_share_link()` |

### Acceptance Criteria
- [ ] **F8.5.1**: Export PNG, PDF, SVG
- [ ] **F8.5.2**: Configurable watermark
- [ ] **F8.5.3**: Share links with expiration

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 8 - Version 1.0*
