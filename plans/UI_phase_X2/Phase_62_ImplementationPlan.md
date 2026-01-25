# Phase 62: System Health & Hardware Telemetry Monitoring

> **Phase ID**: 62 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Prevents 'Internal Sepsis' by monitoring the physical nervous system of the AI brain.

---

## Overview

Diagnostic hub for the infrastructure supporting the autonomous swarm.

---

## Sub-Deliverable 62.1: Kafka Cluster Health & Topic Latency Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/KafkaHealth.jsx` | Cluster monitor |
| `[NEW]` | `frontend2/src/widgets/System/KafkaHealth.css` | Styling |
| `[NEW]` | `frontend2/src/stores/systemStore.js` | System state |
| `[NEW]` | `services/monitoring/kafka_health_service.py` | Kafka metrics |
| `[NEW]` | `web/api/system_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **Messages Per Second**
   - [ ] Real-time scrolling bar chart per topic
   - [ ] Color-coded by topic type (Market, Signal, Risk)
   - [ ] Historical 24h comparison overlay

2. **Consumer Lag Alerts**
   - [ ] Red-alert when lag > 2,000 messages
   - [ ] Taskbar notification integration
   - [ ] Auto-scaling recommendation

3. **Restart Controls**
   - [ ] Zustand-based 'Restart Consumer' toggle
   - [ ] No full system reboot required
   - [ ] Confirmation modal with impact assessment

### Test Coverage Target: **80%**

---

## Sub-Deliverable 62.2: Database I/O & Memory Pressure Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/DBHealth.jsx` | Database monitor |
| `[NEW]` | `frontend2/src/widgets/System/DBHealth.css` | Styling |

### Verbose Acceptance Criteria

1. **Pressure Gauges**
   - [ ] Postgres WAL utilization gauge
   - [ ] Neo4j Page Cache gauge
   - [ ] Visual gradient from green to red

2. **Query Explorer**
   - [ ] Slow-query log with EXPLAIN plans
   - [ ] Cypher and SQL optimization hints
   - [ ] One-click query cancellation

3. **Disk Space Alerts**
   - [ ] Critical alert at 85% utilization
   - [ ] Automated cleanup triggers available
   - [ ] Archive old data options

### Test Coverage Target: **80%**

---

## Sub-Deliverable 62.3: Agent 'Brain' Load Balancer UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/AgentLoadBalancer.jsx` | Process viewer |
| `[NEW]` | `frontend2/src/widgets/System/AgentLoadBalancer.css` | Styling |

### Verbose Acceptance Criteria

1. **Swarm Visualization**
   - [ ] Dynamic tree of active PIDs and heartbeats
   - [ ] CPU/RAM per agent persona
   - [ ] Visual health indicators

2. **Scaling Controls**
   - [ ] One-click 'Scale Up/Down' buttons
   - [ ] Allocate more compute to StackerAgent during volatility
   - [ ] Resource limits enforcement

3. **Prometheus Integration**
   - [ ] Grafana metrics via secure proxy
   - [ ] High-fidelity telemetry charts
   - [ ] Custom dashboard embedding

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/architect/system`

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 62 |
