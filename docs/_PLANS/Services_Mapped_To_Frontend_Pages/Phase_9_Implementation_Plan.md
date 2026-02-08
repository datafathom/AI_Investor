# Phase 9 Implementation Plan: Agent Fleet Command Center

> **Phase**: 9 of 33 | **Status**: 🔴 Not Started | **Priority**: CRITICAL  
> **Duration**: 5 days | **Dependencies**: Phase 1

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `agents` | `fleet_manager.py`, `heartbeat_service.py`, `rogue_killer.py` |
| `coordination` | `task_queue.py`, `dispatcher.py` |

---

## Deliverable 1: Agent Fleet Overview Page

### Frontend: `AgentFleetOverview.jsx`, `AgentCard.jsx`, `DepartmentGrid.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/agents` | `list_all_agents()` |
| GET | `/api/v1/agents/{agent_id}` | `get_agent_details()` |
| POST | `/api/v1/agents/{agent_id}/restart` | `restart_agent()` |

### Acceptance Criteria
- [ ] **F9.1.1**: Grid shows all 84 agents organized by department
- [ ] **F9.1.2**: Status indicators (alive/dead/busy)
- [ ] **F9.1.3**: Click agent for configuration panel
- [ ] **F9.1.4**: Restart button with confirmation
- [ ] **F9.1.5**: Filter by department, status, role

---

## Deliverable 2: Heartbeat Monitor Widget

### Frontend: `HeartbeatWidget.jsx`, `AgentPulseChart.jsx`, `DeadAgentAlert.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/agents/heartbeats` | `get_all_heartbeats()` |
| WS | `/ws/agents/heartbeats` | `stream_heartbeats()` |

### Acceptance Criteria
- [ ] **F9.2.1**: Real-time pulse visualization per agent
- [ ] **F9.2.2**: Alert triggers within 10s of agent death
- [ ] **F9.2.3**: Historical uptime percentage shown
- [ ] **F9.2.4**: Auto-restart option for dead agents
- [ ] **F9.2.5**: Heartbeat latency histogram

---

## Deliverable 3: Rogue Agent Detector Widget

### Frontend: `RogueDetectorWidget.jsx`, `TPMGauge.jsx`, `KillHistoryTable.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/agents/rogue/status` | `get_rogue_status()` |
| GET | `/api/v1/agents/rogue/kills` | `get_kill_history()` |
| POST | `/api/v1/agents/{agent_id}/kill` | `kill_agent()` |

### Acceptance Criteria
- [ ] **F9.3.1**: TPM gauge per agent with threshold line
- [ ] **F9.3.2**: Kill history shows timestamp, agent, reason
- [ ] **F9.3.3**: Manual kill button for emergency shutdown
- [ ] **F9.3.4**: Root cause analysis for each kill
- [ ] **F9.3.5**: Configurable TPM threshold per agent

---

## Deliverable 4: Agent Task Queue Page

### Frontend: `AgentTaskQueue.jsx`, `TaskTable.jsx`, `TaskDetailPanel.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/coordination/tasks` | `list_tasks()` |
| GET | `/api/v1/coordination/tasks/{task_id}` | `get_task_details()` |
| POST | `/api/v1/coordination/tasks/{task_id}/cancel` | `cancel_task()` |
| POST | `/api/v1/coordination/tasks/{task_id}/retry` | `retry_task()` |

### Acceptance Criteria
- [ ] **F9.4.1**: Table shows pending, running, completed tasks
- [ ] **F9.4.2**: Filter by status, agent, priority
- [ ] **F9.4.3**: Task detail shows inputs, outputs, duration
- [ ] **F9.4.4**: Cancel running tasks with confirmation
- [ ] **F9.4.5**: Retry failed tasks with modified params

---

## Deliverable 5: Agent Logs Viewer Panel

### Frontend: `AgentLogsPanel.jsx`, `LogStream.jsx`, `LogLevelFilter.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/agents/{agent_id}/logs` | `get_agent_logs()` |
| WS | `/ws/agents/{agent_id}/logs` | `stream_agent_logs()` |

### Acceptance Criteria
- [ ] **F9.5.1**: Real-time log streaming per agent
- [ ] **F9.5.2**: Filter by log level (DEBUG, INFO, WARN, ERROR)
- [ ] **F9.5.3**: Full-text search within logs
- [ ] **F9.5.4**: Export logs as file
- [ ] **F9.5.5**: Timestamp-based navigation

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 9 - Version 1.0*
