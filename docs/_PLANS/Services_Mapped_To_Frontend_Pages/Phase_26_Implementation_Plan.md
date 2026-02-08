# Phase 26 Implementation Plan: Advanced Order Types & Algos

> **Phase**: 26 of 33 | **Status**: 🔴 Not Started | **Priority**: MEDIUM  
> **Duration**: 5 days | **Dependencies**: Phase 14

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `orders` | `algo_engine.py`, `twap_vwap.py`, `iceberg_slicer.py`, `bracket_manager.py` |

---

## Deliverable 1: Algorithmic Order Entry Page

### Frontend: `AlgoOrderEntry.jsx`, `StrategySelector.jsx`, `ParameterForm.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/orders/algo` | `submit_algo_order()` |
| GET | `/api/v1/orders/algo/strategies` | `list_algo_strategies()` |

### Acceptance Criteria
- [ ] **F26.1.1**: Support TWAP, VWAP, POV (Percent of Volume)
- [ ] **F26.1.2**: Dynamic parameters per algo type
- [ ] **F26.1.3**: Start/End time scheduling
- [ ] **F26.1.4**: Aggression level slider (Passive -> Aggressive)
- [ ] **F26.1.5**: Visual preview of expected execution path

---

## Deliverable 2: Iceberg Order Slicer Widget

### Frontend: `IcebergSlicer.jsx`, `VisibilityControl.jsx`, `VarianceSetting.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/orders/iceberg` | `submit_iceberg()` |

### Acceptance Criteria
- [ ] **F26.2.1**: Large order splitting into child orders
- [ ] **F26.2.2**: Display size configuration
- [ ] **F26.2.3**: Random variance to hide pattern
- [ ] **F26.2.4**: Child order status tracking
- [ ] **F26.2.5**: Reload logic customization

---

## Deliverable 3: Bracket Order Manager Page

### Frontend: `BracketManager.jsx`, `VisualBracket.jsx`, `OrderLineDragger.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/orders/bracket` | `submit_bracket()` |
| PATCH | `/api/v1/orders/bracket/{id}` | `update_bracket()` |

### Acceptance Criteria
- [ ] **F26.3.1**: Entry with attached Take Profit and Stop Loss
- [ ] **F26.3.2**: OCO (One Cancels Other) logic enforcement
- [ ] **F26.3.3**: Drag-and-drop adjustment on chart
- [ ] **F26.3.4**: Risk/Reward ratio calculation displayed
- [ ] **F26.3.5**: Trailing stop configuration

---

## Deliverable 4: Multi-Leg Strategy Builder

### Frontend: `MultiLegBuilder.jsx`, `LegRow.jsx`, `PayoffDiagram.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/orders/multileg` | `submit_multileg()` |
| GET | `/api/v1/orders/multileg/preview` | `quote_multileg()` |
| GET | `/api/v1/orders/multileg/templates` | `get_spread_templates()` |

### Acceptance Criteria
- [ ] **F26.4.1**: Vertical, Calendar, Diagonal spread presets
- [ ] **F26.4.2**: Iron Condor, Butterfly, Straddle templates
- [ ] **F26.4.3**: Complex net price limit order
- [ ] **F26.4.4**: Leg-by-leg fill status
- [ ] **F26.4.5**: Theoretical P&L graph at expiry

---

## Deliverable 5: Dark Pool & Block Trade Access

### Frontend: `DarkPoolAccess.jsx`, `LiquiditySeeker.jsx`, `IndicationOfInterest.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/orders/dark/venues` | `list_dark_venues()` |
| POST | `/api/v1/orders/dark/route` | `route_to_dark_pool()` |

### Acceptance Criteria
- [ ] **F26.5.1**: Venue selection (IEX, Sigma X, etc.)
- [ ] **F26.5.2**: Min quantity condition
- [ ] **F26.5.3**: Dark liquidity seeking logic
- [ ] **F26.5.4**: Anti-gaming logic toggles
- [ ] **F26.5.5**: Report on price improvement vs lit markets

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 26 - Version 1.0*
