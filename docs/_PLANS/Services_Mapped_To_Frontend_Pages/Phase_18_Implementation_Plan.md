# Phase 18 Implementation Plan: Watchlist & Opportunity Management

> **Phase**: 18 of 33 | **Status**: 🔴 Not Started | **Priority**: HIGH  
> **Duration**: 4 days | **Dependencies**: Phase 4, Phase 6

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `watchlist` | `manager.py`, `alert_service.py`, `opportunity_tracker.py`, `screener_engine.py`, `share_service.py` |

---

## Deliverable 1: Enhanced Watchlist Manager

### Frontend: `WatchlistManager.jsx`, `SymbolGrid.jsx`, `TagEditor.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/watchlist` | `list_watchlists()` |
| POST | `/api/v1/watchlist` | `create_watchlist()` |
| PUT | `/api/v1/watchlist/{id}/symbols` | `update_symbols()` |
| DELETE | `/api/v1/watchlist/{id}` | `delete_watchlist()` |

### Acceptance Criteria
- [ ] **F18.1.1**: Create/Edit/Delete multiple named watchlists
- [ ] **F18.1.2**: Drag-and-drop symbol reordering
- [ ] **F18.1.3**: Custom columns (Price, Change, RSI, Volume)
- [ ] **F18.1.4**: Tagging system for symbols
- [ ] **F18.1.5**: Import symbols from CSV/Clipboard

---

## Deliverable 2: Price Alert Center

### Frontend: `AlertCenter.jsx`, `AlertRuleBuilder.jsx`, `ActiveAlertsList.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/watchlist/alerts` | `get_active_alerts()` |
| POST | `/api/v1/watchlist/alerts` | `create_alert()` |
| DELETE | `/api/v1/watchlist/alerts/{id}` | `delete_alert()` |
| GET | `/api/v1/watchlist/alerts/history` | `get_alert_history()` |

### Acceptance Criteria
- [ ] **F18.2.1**: Simple price alerts (Above/Below)
- [ ] **F18.2.2**: Complex indicator alerts (RSI > 70 AND Price < SMA50)
- [ ] **F18.2.3**: Push notification configuration
- [ ] **F18.2.4**: Alert triggers shown on charts
- [ ] **F18.2.5**: Snooze and recurring options

---

## Deliverable 3: Opportunity Tracker

### Frontend: `OpportunityTracker.jsx`, `ThesisEditor.jsx`, `StatusBoard.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/watchlist/opportunities` | `list_opportunities()` |
| POST | `/api/v1/watchlist/opportunities` | `create_opportunity()` |
| PUT | `/api/v1/watchlist/opportunities/{id}` | `update_opportunity()` |

### Acceptance Criteria
- [ ] **F18.3.1**: Kanban board for ideas (New, Researching, Ready, Active, Closed)
- [ ] **F18.3.2**: Investment thesis rich text editor
- [ ] **F18.3.3**: Link to charts and research notes
- [ ] **F18.3.4**: Conviction scoring (1-10)
- [ ] **F18.3.5**: Outcome tracking for closed opportunities

---

## Deliverable 4: Screener Builder

### Frontend: `ScreenerBuilder.jsx`, `CriteriaSelector.jsx`, `ResultsGrid.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/watchlist/screener/run` | `run_screen()` |
| POST | `/api/v1/watchlist/screener/save` | `save_screen()` |
| GET | `/api/v1/watchlist/screener/saved` | `list_screens()` |

### Acceptance Criteria
- [ ] **F18.4.1**: Multi-factor screening (Technical + Fundamental)
- [ ] **F18.4.2**: Real-time result updates
- [ ] **F18.4.3**: Save screen criteria as preset
- [ ] **F18.4.4**: "Add All Results to Watchlist" action
- [ ] **F18.4.5**: Pre-built popular screens (Top Gainers, Oversold)

---

## Deliverable 5: Watchlist Sharing

### Frontend: `ShareWatchlistModal.jsx`, `CollaboratorList.jsx`, `PublicLinkSetting.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/watchlist/{id}/share` | `share_watchlist()` |
| GET | `/api/v1/watchlist/shared/{token}` | `get_shared_watchlist()` |

### Acceptance Criteria
- [ ] **F18.5.1**: Share with specific team members via email
- [ ] **F18.5.2**: Generate public read-only link
- [ ] **F18.5.3**: Permission levels (View vs Edit)
- [ ] **F18.5.4**: Real-time sync for collaborators
- [ ] **F18.5.5**: Copy shared watchlist to my lists

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 18 - Version 1.0*
