# Phase 19 Implementation Plan: Risk Management Console

> **Phase**: 19 of 33 | **Status**: 🔴 Not Started | **Priority**: CRITICAL  
> **Duration**: 5 days | **Dependencies**: Phase 4, Phase 14

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `risk` | `risk_aggregator.py`, `position_sizer.py`, `correlation_monitor.py`, `limit_manager.py` |
| `fraud` | `detection_engine.py` |

---

## Deliverable 1: Risk Dashboard

### Frontend: `RiskDashboard.jsx`, `VaRGauge.jsx`, `ExposureBreakdown.jsx`, `HeatmapWidget.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/risk/summary` | `get_risk_summary()` |
| GET | `/api/v1/risk/var` | `get_var_metrics()` |
| GET | `/api/v1/risk/exposures` | `get_exposures()` |

### Acceptance Criteria
- [ ] **F19.1.1**: Portfolio-wide VaR (95% & 99%)
- [ ] **F19.1.2**: Exposure by asset class, sector, geography
- [ ] **F19.1.3**: Leverage and margin usage indicators
- [ ] **F19.1.4**: Beta-weighted portfolio delta
- [ ] **F19.1.5**: Drawdown tracking from HWM

---

## Deliverable 2: Position Sizing Calculator Widget

### Frontend: `PositionSizer.jsx`, `RiskParameterForm.jsx`, `SizeRecommendation.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/risk/sizing/calculate` | `calculate_position_size()` |

### Acceptance Criteria
- [ ] **F19.2.1**: Kelly Criterion calculator
- [ ] **F19.2.2**: Fixed Fractional sizing logic
- [ ] **F19.2.3**: Volatility-adjusted sizing
- [ ] **F19.2.4**: Max loss constraint validation
- [ ] **F19.2.5**: Comparison of sizing methods

---

## Deliverable 3: Correlation Risk Monitor Page

### Frontend: `CorrelationRisk.jsx`, `CorrelationMatrix.jsx`, `ClusterAnalysis.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/risk/correlations` | `get_portfolio_correlations()` |
| GET | `/api/v1/risk/clusters` | `get_asset_clusters()` |

### Acceptance Criteria
- [ ] **F19.3.1**: Real-time correlation matrix of holdings
- [ ] **F19.3.2**: Hierarchical clustering visualization
- [ ] **F19.3.3**: Alert on correlation breakdown/spike
- [ ] **F19.3.4**: Diversification score
- [ ] **F19.3.5**: Scenario-based correlation stress testing

---

## Deliverable 4: Fraud Detection Center Page

### Frontend: `FraudCenter.jsx`, `AlertsTable.jsx`, `UserActivityLog.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/fraud/alerts` | `get_fraud_alerts()` |
| POST | `/api/v1/fraud/activity` | `log_activity()` |
| GET | `/api/v1/fraud/settings` | `get_detection_settings()` |

### Acceptance Criteria
- [ ] **F19.4.1**: Real-time flagging of suspicious transactions
- [ ] **F19.4.2**: Login anomaly detection (IP/Device)
- [ ] **F19.4.3**: Workflow for alert investigation/resolution
- [ ] **F19.4.4**: Whitelist management
- [ ] **F19.4.5**: ML-based anomaly score

---

## Deliverable 5: Risk Limit Manager Page

### Frontend: `RiskLimitManager.jsx`, `LimitTable.jsx`, `ViolationLog.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/risk/limits` | `get_risk_limits()` |
| PUT | `/api/v1/risk/limits/{id}` | `update_risk_limit()` |
| GET | `/api/v1/risk/violations` | `get_violations()` |

### Acceptance Criteria
- [ ] **F19.5.1**: Define Gross/Net exposure limits
- [ ] **F19.5.2**: Set single-position max weight
- [ ] **F19.5.3**: Daily Drawdown Stop-Loss config
- [ ] **F19.5.4**: Concentration limit enforcement
- [ ] **F19.5.5**: Automated trading halt on limit breach

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 19 - Version 1.0*
