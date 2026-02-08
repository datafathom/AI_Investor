# Phase 10 Implementation Plan: AI Debate & Consensus System

> **Phase**: 10 of 33 | **Status**: 🔴 Not Started | **Priority**: CRITICAL  
> **Duration**: 5 days | **Dependencies**: Phase 9

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `agents.debate_orchestrator` | `debate_orchestrator.py` |
| `agents.consensus_engine` | `consensus_engine.py` |
| `debate` | `history_service.py`, `verdict_tracker.py` |

---

## Deliverable 1: Debate Arena Page

### Frontend: `DebateArena.jsx`, `DebateFeed.jsx`, `ParticipantCard.jsx`, `SentimentMeter.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/debate/sessions` | `start_debate()` |
| GET | `/api/v1/debate/sessions/{id}` | `get_debate_session()` |
| GET | `/api/v1/debate/sessions/{id}/turns` | `get_debate_turns()` |
| WS | `/ws/debate/{session_id}` | `stream_debate()` |

### Acceptance Criteria
- [ ] **F10.1.1**: Live Bull vs Bear debate visualization
- [ ] **F10.1.2**: Turn-by-turn transcript with confidence scores
- [ ] **F10.1.3**: Participant cards show agent name, persona, stance
- [ ] **F10.1.4**: Real-time sentiment score evolution
- [ ] **F10.1.5**: Debate controls (pause, resume, end)

---

## Deliverable 2: Consensus Voting Panel

### Frontend: `ConsensusVotingPanel.jsx`, `VoteGauge.jsx`, `VoteBreakdownChart.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/consensus/{session_id}/votes` | `get_votes()` |
| GET | `/api/v1/consensus/{session_id}/result` | `get_consensus_result()` |
| POST | `/api/v1/consensus/{session_id}/override` | `human_override()` |

### Acceptance Criteria
- [ ] **F10.2.1**: Vote tally with approval percentage
- [ ] **F10.2.2**: Breakdown by persona type
- [ ] **F10.2.3**: Threshold line (70% default)
- [ ] **F10.2.4**: Human override capability
- [ ] **F10.2.5**: Vote confidence weights

---

## Deliverable 3: Debate History Browser Page

### Frontend: `DebateHistory.jsx`, `DebateListTable.jsx`, `TranscriptViewer.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/debate/history` | `list_past_debates()` |
| GET | `/api/v1/debate/history/{id}/transcript` | `get_transcript()` |
| GET | `/api/v1/debate/history/{id}/outcome` | `get_debate_outcome()` |

### Acceptance Criteria
- [ ] **F10.3.1**: Searchable list of past debates
- [ ] **F10.3.2**: Filter by ticker, outcome, date
- [ ] **F10.3.3**: Full transcript with turn navigation
- [ ] **F10.3.4**: Outcome summary with performance impact
- [ ] **F10.3.5**: Export transcript as PDF

---

## Deliverable 4: Human Intervention Modal

### Frontend: `HumanInterventionModal.jsx`, `ArgumentInput.jsx`, `ImpactPreview.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/debate/sessions/{id}/intervene` | `inject_human_argument()` |
| GET | `/api/v1/debate/sessions/{id}/impact` | `preview_impact()` |

### Acceptance Criteria
- [ ] **F10.4.1**: Text input for user argument
- [ ] **F10.4.2**: Preview impact on current sentiment
- [ ] **F10.4.3**: Argument injected as new turn
- [ ] **F10.4.4**: Weight selector (light/moderate/heavy)
- [ ] **F10.4.5**: Confirmation before injection

---

## Deliverable 5: Verdict Tracker Widget

### Frontend: `VerdictTrackerWidget.jsx`, `SentimentChart.jsx`, `VerdictBadge.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/debate/sessions/{id}/verdict` | `get_current_verdict()` |
| WS | `/ws/debate/{id}/sentiment` | `stream_sentiment()` |

### Acceptance Criteria
- [ ] **F10.5.1**: Real-time sentiment score (-100 to +100)
- [ ] **F10.5.2**: Verdict badge (BULLISH/BEARISH/NEUTRAL)
- [ ] **F10.5.3**: Historical sentiment evolution chart
- [ ] **F10.5.4**: Turning point markers on chart
- [ ] **F10.5.5**: Confidence interval bands

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 10 - Version 1.0*
