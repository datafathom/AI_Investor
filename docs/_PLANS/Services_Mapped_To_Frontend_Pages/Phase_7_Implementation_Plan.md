# Phase 7 Implementation Plan: Research & Analytics Platform

> **Phase**: 7 of 33  
> **Status**: 🔴 Not Started  
> **Priority**: HIGH  
> **Estimated Duration**: 6 days  
> **Dependencies**: Phase 4, Phase 5, Phase 6

---

## Overview

Phase 7 builds the research and analytics platform including a research workspace, factor analysis, fundamental screening, sector rotation analysis, and quantitative backtesting.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `research` | `services/research/` | `workspace.py`, `notebook_runner.py` |
| `analysis` | `services/analysis/` | `fundamental_scanner.py`, `company_analysis.py` |
| `analytics` | `services/analytics/` | `sector_rotation.py`, `performance_attribution.py` |
| `quantitative` | `services/quantitative/` | `factor_engine.py`, `backtest_engine.py` |

---

## Deliverable 1: Research Workspace Page

### 1.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `ResearchWorkspace.jsx` | `frontend/src/pages/data-scientist/ResearchWorkspace.jsx` | Page |
| `NotebookEditor.jsx` | `frontend/src/components/editors/NotebookEditor.jsx` | Editor |
| `CodeCell.jsx` | `frontend/src/components/cells/CodeCell.jsx` | Widget |
| `OutputCell.jsx` | `frontend/src/components/cells/OutputCell.jsx` | Widget |
| `NotebookSidebar.jsx` | `frontend/src/components/sidebars/NotebookSidebar.jsx` | Sidebar |
| `EnvironmentSelector.jsx` | `frontend/src/components/selectors/EnvironmentSelector.jsx` | Selector |

### 1.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/research/notebooks` | `list_notebooks()` |
| POST | `/api/v1/research/notebooks` | `create_notebook()` |
| GET | `/api/v1/research/notebooks/{id}` | `get_notebook()` |
| PUT | `/api/v1/research/notebooks/{id}` | `save_notebook()` |
| POST | `/api/v1/research/notebooks/{id}/execute` | `execute_cell()` |
| GET | `/api/v1/research/environments` | `list_environments()` |

### 1.3 End-to-End Acceptance Criteria

- [ ] **F7.1.1**: Jupyter-like interface with code and markdown cells
- [ ] **F7.1.2**: Python code execution in sandboxed environment
- [ ] **F7.1.3**: Output renders text, tables, and charts inline
- [ ] **F7.1.4**: Sidebar shows notebook list with folders
- [ ] **F7.1.5**: Environment selector for different Python kernels
- [ ] **I7.1.1**: Execute POST returns async job ID for output polling
- [ ] **I7.1.2**: Auto-save every 30 seconds
- [ ] **R7.1.1**: Notebook schema: `{ id, name, cells[], created_at, modified_at }`
- [ ] **R7.1.2**: Cell output includes stdout, stderr, rich_output

---

## Deliverable 2: Factor Analysis Suite Page

### 2.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `FactorAnalysisSuite.jsx` | `frontend/src/pages/data-scientist/FactorAnalysisSuite.jsx` | Page |
| `FactorExposureChart.jsx` | `frontend/src/components/charts/FactorExposureChart.jsx` | Chart |
| `FactorHeatmap.jsx` | `frontend/src/components/charts/FactorHeatmap.jsx` | Chart |
| `FactorReturnTable.jsx` | `frontend/src/components/tables/FactorReturnTable.jsx` | Table |
| `PortfolioFactorPanel.jsx` | `frontend/src/components/panels/PortfolioFactorPanel.jsx` | Panel |
| `FactorComparisonChart.jsx` | `frontend/src/components/charts/FactorComparisonChart.jsx` | Chart |

### 2.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/quantitative/factors` | `list_factors()` |
| POST | `/api/v1/quantitative/factors/exposure` | `calculate_factor_exposure()` |
| GET | `/api/v1/quantitative/factors/returns` | `get_factor_returns()` |
| POST | `/api/v1/quantitative/factors/portfolio` | `analyze_portfolio_factors()` |
| GET | `/api/v1/quantitative/factors/{factor}/history` | `get_factor_history()` |

### 2.3 End-to-End Acceptance Criteria

- [ ] **F7.2.1**: Heatmap shows factor exposures for portfolio holdings
- [ ] **F7.2.2**: Factor returns table shows Fama-French factors (Mkt, SMB, HML, etc.)
- [ ] **F7.2.3**: Comparison chart overlays multiple factor performance
- [ ] **F7.2.4**: Portfolio panel shows net exposure per factor
- [ ] **F7.2.5**: Historical factor analysis for custom date ranges
- [ ] **I7.2.1**: Exposure calculation includes position weights
- [ ] **I7.2.2**: Factor data updated daily at market close
- [ ] **R7.2.1**: Exposure schema: `{ ticker, factors: { mkt_beta, smb, hml, mom, ... } }`
- [ ] **R7.2.2**: Factor return schema: `{ factor, period_return, cumulative_return }`

---

## Deliverable 3: Fundamental Scanner Page

### 3.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `FundamentalScanner.jsx` | `frontend/src/pages/data-scientist/FundamentalScanner.jsx` | Page |
| `ScannerBuilder.jsx` | `frontend/src/components/builders/ScannerBuilder.jsx` | Widget |
| `MetricSelector.jsx` | `frontend/src/components/selectors/MetricSelector.jsx` | Selector |
| `ScanResultsTable.jsx` | `frontend/src/components/tables/ScanResultsTable.jsx` | Table |
| `CompanyDetailModal.jsx` | `frontend/src/components/modals/CompanyDetailModal.jsx` | Modal |
| `SaveScanModal.jsx` | `frontend/src/components/modals/SaveScanModal.jsx` | Modal |

### 3.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/analysis/metrics` | `list_available_metrics()` |
| POST | `/api/v1/analysis/scan` | `run_fundamental_scan()` |
| GET | `/api/v1/analysis/scans` | `list_saved_scans()` |
| POST | `/api/v1/analysis/scans` | `save_scan()` |
| GET | `/api/v1/analysis/companies/{ticker}` | `get_company_fundamentals()` |

### 3.3 End-to-End Acceptance Criteria

- [ ] **F7.3.1**: Builder allows multiple metric conditions (P/E < 15 AND ROE > 20)
- [ ] **F7.3.2**: Metric selector shows 50+ fundamental metrics
- [ ] **F7.3.3**: Results table sortable by any metric column
- [ ] **F7.3.4**: Company modal shows detailed fundamentals with charts
- [ ] **F7.3.5**: Save and schedule scans for daily/weekly alerts
- [ ] **I7.3.1**: Scan POST returns paginated results
- [ ] **I7.3.2**: Fundamentals include TTM and MRQ values
- [ ] **R7.3.1**: Metric schema: `{ id, name, category, description, format }`
- [ ] **R7.3.2**: Scan result schema: `{ ticker, company_name, metrics: {...} }`

---

## Deliverable 4: Sector Rotation Model Widget

### 4.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `SectorRotationWidget.jsx` | `frontend/src/components/widgets/SectorRotationWidget.jsx` | Widget |
| `SectorMomentumChart.jsx` | `frontend/src/components/charts/SectorMomentumChart.jsx` | Chart |
| `RotationSignalCard.jsx` | `frontend/src/components/cards/RotationSignalCard.jsx` | Card |
| `SectorPerformanceTable.jsx` | `frontend/src/components/tables/SectorPerformanceTable.jsx` | Table |
| `CyclePhaseIndicator.jsx` | `frontend/src/components/indicators/CyclePhaseIndicator.jsx` | Indicator |

### 4.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/analytics/sector-rotation` | `get_sector_rotation()` |
| GET | `/api/v1/analytics/sector-rotation/signals` | `get_rotation_signals()` |
| GET | `/api/v1/analytics/sectors/performance` | `get_sector_performance()` |
| GET | `/api/v1/analytics/cycle/phase` | `get_business_cycle_phase()` |

### 4.3 End-to-End Acceptance Criteria

- [ ] **F7.4.1**: Momentum chart shows relative sector performance
- [ ] **F7.4.2**: Signal cards show rotate-into and rotate-out-of sectors
- [ ] **F7.4.3**: Performance table ranks sectors by 1m/3m/6m/1y returns
- [ ] **F7.4.4**: Cycle phase indicator shows Early/Mid/Late/Recession
- [ ] **F7.4.5**: Historical rotation signals with backtest results
- [ ] **I7.4.1**: Rotation model updated weekly
- [ ] **I7.4.2**: Cycle phase derived from economic indicators
- [ ] **R7.4.1**: Rotation schema: `{ into_sectors[], out_of_sectors[], confidence }`
- [ ] **R7.4.2**: Sector performance: `{ sector, return_1m, return_3m, return_6m, return_1y }`

---

## Deliverable 5: Quant Backtest Lab Page

### 5.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `QuantBacktestLab.jsx` | `frontend/src/pages/data-scientist/QuantBacktestLab.jsx` | Page |
| `StrategyBuilder.jsx` | `frontend/src/components/builders/StrategyBuilder.jsx` | Widget |
| `BacktestResultsPanel.jsx` | `frontend/src/components/panels/BacktestResultsPanel.jsx` | Panel |
| `EquityCurveChart.jsx` | `frontend/src/components/charts/EquityCurveChart.jsx` | Chart |
| `DrawdownChart.jsx` | `frontend/src/components/charts/DrawdownChart.jsx` | Chart |
| `MonteCarloChart.jsx` | `frontend/src/components/charts/MonteCarloChart.jsx` | Chart |
| `MetricsTable.jsx` | `frontend/src/components/tables/MetricsTable.jsx` | Table |

### 5.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/quantitative/backtest` | `run_backtest()` |
| GET | `/api/v1/quantitative/backtest/{id}` | `get_backtest_results()` |
| GET | `/api/v1/quantitative/backtest/{id}/trades` | `get_backtest_trades()` |
| POST | `/api/v1/quantitative/monte-carlo` | `run_monte_carlo()` |
| GET | `/api/v1/quantitative/strategies` | `list_saved_strategies()` |
| POST | `/api/v1/quantitative/strategies` | `save_strategy()` |

### 5.3 End-to-End Acceptance Criteria

- [ ] **F7.5.1**: Strategy builder with entry/exit conditions
- [ ] **F7.5.2**: Equity curve shows strategy vs benchmark
- [ ] **F7.5.3**: Drawdown chart highlights max drawdown periods
- [ ] **F7.5.4**: Monte Carlo shows 1000-path probability distribution
- [ ] **F7.5.5**: Metrics table: Sharpe, Sortino, Max DD, CAGR, Win Rate
- [ ] **I7.5.1**: Backtest POST async with progress updates
- [ ] **I7.5.2**: Trade log includes entry, exit, P&L, duration
- [ ] **R7.5.1**: Backtest result: `{ equity_curve[], metrics: {...}, trades[] }`
- [ ] **R7.5.2**: Monte Carlo: `{ paths[][], percentiles: { p5, p25, p50, p75, p95 } }`

---

## Testing Requirements

| Test Suite | Description |
|------------|-------------|
| `test_phase7_research_e2e.py` | Create notebook → add cells → execute → save |
| `test_phase7_factors_e2e.py` | Load factors → portfolio exposure → history |
| `test_phase7_scanner_e2e.py` | Build scan → run → company detail |
| `test_phase7_rotation_e2e.py` | Widget load → signals → sector performance |
| `test_phase7_backtest_e2e.py` | Build strategy → backtest → monte carlo |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 7 Implementation Plan - Version 1.0*
