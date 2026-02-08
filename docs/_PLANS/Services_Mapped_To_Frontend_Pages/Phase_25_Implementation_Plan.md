# Phase 25 Implementation Plan: Portfolio Management & Construction

> **Phase**: 25 of 33 | **Status**: 🔴 Not Started | **Priority**: HIGH  
> **Duration**: 5 days | **Dependencies**: Phase 4, Phase 19

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `portfolio` | `manager.py`, `rebalancer.py`, `tax_optimizer.py`, `performance_analyst.py`, `construction_engine.py` |

---

## Deliverable 1: Portfolio Overview Dashboard

### Frontend: `PortfolioOverview.jsx`, `AllocationChart.jsx`, `PerformanceSummary.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/portfolio/summary` | `get_portfolio_summary()` |
| GET | `/api/v1/portfolio/holdings` | `get_current_holdings()` |
| GET | `/api/v1/portfolio/performance` | `get_performance_history()` |

### Acceptance Criteria
- [ ] **F25.1.1**: Total Net Liquidation Value real-time updates
- [ ] **F25.1.2**: Asset allocation donut (Equity, Option, Cash, Crypto)
- [ ] **F25.1.3**: Top movers and portfolio drivers
- [ ] **F25.1.4**: Daily/Weekly/YTD P&L stats
- [ ] **F25.1.5**: Benchmark comparison (SPY, QQQ)

---

## Deliverable 2: Automated Rebalancer Page

### Frontend: `Rebalancer.jsx`, `TargetConfig.jsx`, `AdjustmentPreview.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/portfolio/targets` | `get_allocation_targets()` |
| POST | `/api/v1/portfolio/rebalance/preview` | `preview_rebalance()` |
| POST | `/api/v1/portfolio/rebalance/execute` | `execute_rebalance()` |

### Acceptance Criteria
- [ ] **F25.2.1**: Define target allocation % per asset
- [ ] **F25.2.2**: Drift tolerance settings
- [ ] **F25.2.3**: One-click "Generate Trades" to fix drift
- [ ] **F25.2.4**: Tax-aware rebalancing suggestions
- [ ] **F25.2.5**: Schedule auto-rebalance (Quarterly/Monthly)

---

## Deliverable 3: Tax Loss Harvester Widget

### Frontend: `TaxHarvester.jsx`, `LossOpportunityTable.jsx`, `SwapCandidateSelector.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/portfolio/tax/opportunities` | `scan_harvesting_ops()` |
| POST | `/api/v1/portfolio/tax/harvest` | `execute_harvest()` |

### Acceptance Criteria
- [ ] **F25.3.1**: Scan holdings for unrealized losses > threshold
- [ ] **F25.3.2**: Suggest "Similar but not Identical" replacements
- [ ] **F25.3.3**: Avoid wash sales check
- [ ] **F25.3.4**: Estimate tax savings impact
- [ ] **F25.3.5**: Batch execute harvest trades

---

## Deliverable 4: Performance Attribution Page

### Frontend: `PerformanceAttribution.jsx`, `BrinsonFachlerChart.jsx`, `FactorAttribTable.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/portfolio/analysis/attribution` | `get_attribution()` |

### Acceptance Criteria
- [ ] **F25.4.1**: Brinson analysis (Allocation vs Selection effect)
- [ ] **F25.4.2**: Return contribution by Sector
- [ ] **F25.4.3**: Alpha generation metrics
- [ ] **F25.4.4**: Return vs Risk scatter plot (Holdings)
- [ ] **F25.4.5**: Time-weighted vs Money-weighted return

---

## Deliverable 5: Portfolio Construction Lab

### Frontend: `ConstructionLab.jsx`, `EfficientFrontierChart.jsx`, `OptimizationConstraints.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/portfolio/optimize` | `run_optimization()` |
| GET | `/api/v1/portfolio/frontier` | `get_efficient_frontier()` |

### Acceptance Criteria
- [ ] **F25.5.1**: Mean-Variance Optimization engine
- [ ] **F25.5.2**: Black-Litterman model support
- [ ] **F25.5.3**: Efficient Frontier visualization with current portfolio dot
- [ ] **F25.5.4**: Custom constraints (Min/Max weight, No Short)
- [ ] **F25.5.5**: Save optimized weights as new target

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 25 - Version 1.0*
