# Phase 29 Implementation Plan: AI Portfolio Reporting & Tax

> **Phase**: 29 of 33 | **Status**: 🔴 Not Started | **Priority**: HIGH  
> **Duration**: 5 days | **Dependencies**: Phase 22, Phase 25

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `reporting` | `pdf_generator.py`, `ai_commentary.py`, `performance_attribution.py` |
| `tax` | `tax_estimator.py`, `harvesting_service.py`, `form_1099_preview.py` |

---

## Deliverable 1: AI-Generated Executive Summary

### Frontend: `ExecSummaryPage.jsx`, `AIInsightsCard.jsx`, `MetricTrendArrows.jsx`, `VoiceSummaryButton.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/reporting/executive-summary` | `get_ai_summary()` |
| POST | `/api/v1/reporting/narrative/regenerate` | `refresh_commentary()` |

### Acceptance Criteria
- [ ] **F29.1.1**: Natural language summary of portfolio performance (LLM powered)
- [ ] **F29.1.2**: Identification of the "Top 3 Things to Watch"
- [ ] **F29.1.3**: Tone adjustment (Institutional, Casual, or Emergency/Urgent)
- [ ] **F29.1.4**: Highlight correlation breakthroughs and outlier events
- [ ] **F29.1.5**: Click-to-explain deep dive for any AI-generated claim

---

## Deliverable 2: Professional PDF Report Builder

### Frontend: `ReportBuilder.jsx`, `TemplateSelector.jsx`, `LayoutDragDrop.jsx`, `BrandingPanel.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/reporting/generate-pdf` | `build_pdf_report()` |
| GET | `/api/v1/reporting/templates` | `list_report_templates()` |

### Acceptance Criteria
- [ ] **F29.2.1**: Choose between Quarterly Review, Tax Report, or Deep Dive Alpha report
- [ ] **F29.2.2**: Drag-and-drop charts/tables into custom layout
- [ ] **F29.2.3**: Custom branding (Logo, Colors, Disclaimer, Header/Footer)
- [ ] **F29.2.4**: Page break management and Table of Contents generation
- [ ] **F29.2.5**: Async generation with progress bar and "Email me when ready" button

---

## Deliverable 3: Tax Liability & Estimate Dashboard

### Frontend: `TaxLiabilityDashboard.jsx`, `GainsHeatmap.jsx`, `EstimateTable.jsx`, `SafeHarborWidget.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/tax/liabilities/estimated` | `calculate_tax_estimates()` |
| GET | `/api/v1/tax/lots/harvesting` | `list_harvesting_opportunities()` |

### Acceptance Criteria
- [ ] **F29.3.1**: Real-time federal/state capital gains tax estimation
- [ ] **F29.3.2**: Short-term vs Long-term breakdown with rate switches
- [ ] **F29.3.3**: Safe Harbor calculation and quarterly payment tracker
- [ ] **F29.3.4**: Wash sale disallowed loss warnings across all connected accounts
- [ ] **F29.3.5**: Tax projection for various liquidation scenarios

---

## Deliverable 4: Portfolio Attribution Analysis Page

### Frontend: `AttributionAnalysis.jsx`, `SectorSelectionChart.jsx`, `FactorReturnDrilldown.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/portfolio/attribution` | `get_performance_attribution()` |

### Acceptance Criteria
- [ ] **F29.4.1**: Brinson-Fachler attribution (Allocation vs Selection vs Interaction)
- [ ] **F29.4.2**: Return contribution by sector, asset class, and individual ticker
- [ ] **F29.4.3**: Active share calculation vs benchmark
- [ ] **F29.4.4**: Fee drag impact on net returns visualization
- [ ] **F29.4.5**: Performance persistence analysis over multiple time periods

---

## Deliverable 5: Investor Portal & Sharing Center

### Frontend: `InvestorPortal.jsx`, `PermissionSettings.jsx`, `SharedLinkTable.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/reporting/share` | `create_secure_share_link()` |
| GET | `/api/v1/reporting/access-logs` | `list_report_views()` |

### Acceptance Criteria
- [ ] **F29.5.1**: Generate secure, time-limited, password-protected report links
- [ ] **F29.5.2**: Granular permissions (Hide specific accounts, hide tax data, read-only)
- [ ] **F29.5.3**: Audit log of who accessed which report and when
- [ ] **F29.5.4**: Portfolio heartbeat feature (share live limited view with spouse/partner)
- [ ] **F29.5.5**: One-click "Pause all sharing" emergency button

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 29 - Version 1.0*
