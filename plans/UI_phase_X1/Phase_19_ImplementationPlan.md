# Phase 19: System Health & Hardware Telemetry Monitoring

> **Phase 62** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Prevents 'Internal Sepsis' by monitoring the physical nervous system of the AI brain.

---

## Overview

Diagnostic hub for the infrastructure supporting the autonomous swarm, ensuring system reliability.

---

## Sub-Deliverable 62.1: Kafka Cluster Health & Topic Latency Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/KafkaHealth.jsx` | Health dashboard |
| `[NEW]` | `frontend2/src/widgets/System/KafkaHealth.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/System/TopicLatency.jsx` | Per-topic view |
| `[NEW]` | `frontend2/src/services/metricsService.js` | Metrics API |

### Verbose Acceptance Criteria

1. **Messages Per Second Visualization**
   - [ ] Real-time scrolling bar chart per topic
   - [ ] Historical trend (last 5 minutes)
   - [ ] Sparkline for each topic row
   - [ ] Total throughput summary

2. **Consumer Lag Alerting**
   - [ ] Red alert for any consumer group with lag >2,000 messages
   - [ ] Consumer group list with lag counts
   - [ ] Trend: increasing/stable/decreasing
   - [ ] "Lag Spike" notification

3. **Restart Consumer Toggle**
   - [ ] Zustand-based "Restart Consumer" action
   - [ ] Confirmation modal before restart
   - [ ] Status feedback after restart
   - [ ] Restart history log

4. **Cluster Overview**
   - [ ] Broker count and health status
   - [ ] Partition distribution
   - [ ] Replication factor
   - [ ] ISR (In-Sync Replicas) count

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/metrics/kafka` | GET | Kafka cluster metrics |
| `/api/v1/kafka/consumers/:group/restart` | POST | Restart consumer |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `KafkaHealth.test.jsx` | Dashboard renders, lag alerts show |
| `TopicLatency.test.jsx` | Per-topic metrics, sparklines |
| `metricsService.test.js` | API parsing, error handling |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 62.2: Database I/O & Memory Pressure Gauges

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/DatabaseGauges.jsx` | DB metrics widget |
| `[NEW]` | `frontend2/src/widgets/System/DatabaseGauges.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/System/SlowQueryLog.jsx` | Slow query viewer |

### Verbose Acceptance Criteria

1. **Postgres WAL Pressure Gauge**
   - [ ] Visual gauge for Write-Ahead Log usage
   - [ ] Threshold markers: Normal, Warning, Critical
   - [ ] Historical trend chart
   - [ ] WAL archive status

2. **Neo4j Page Cache Gauge**
   - [ ] Page cache hit ratio gauge
   - [ ] Target: >99% hit rate
   - [ ] Memory allocation display
   - [ ] Eviction rate monitoring

3. **Slow Query Log Explorer**
   - [ ] List queries exceeding threshold (100ms default)
   - [ ] EXPLAIN plan visualization for each query
   - [ ] Query optimization suggestions
   - [ ] Filter by database, table, time

4. **Disk Space Alerts**
   - [ ] Alert when disk utilization exceeds 85%
   - [ ] Per-database breakdown
   - [ ] Growth projection
   - [ ] "Cleanup Suggestions" button

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DatabaseGauges.test.jsx` | Gauges render, thresholds work |
| `SlowQueryLog.test.jsx` | Queries list, EXPLAIN display |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 62.3: Agent 'Brain' Load Balancer UI

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/System/AgentLoadBalancer.jsx` | Load balancer widget |
| `[NEW]` | `frontend2/src/widgets/System/AgentLoadBalancer.css` | Styling |
| `[NEW]` | `frontend2/src/widgets/System/ProcessTree.jsx` | PID tree view |

### Verbose Acceptance Criteria

1. **Dynamic PID Tree Visualization**
   - [ ] Tree view of all active agent processes
   - [ ] CPU/RAM per process
   - [ ] Parent-child relationships
   - [ ] Expand/collapse branches

2. **Scale Up/Down Actions**
   - [ ] One-click scale allocation
   - [ ] Allocate more compute to "StackerAgent" during volatility
   - [ ] Resource limits per agent type
   - [ ] Auto-scaling rules configuration

3. **Prometheus/Grafana Integration**
   - [ ] Secure proxy to Prometheus metrics
   - [ ] Embedded Grafana panels
   - [ ] Custom dashboard links
   - [ ] Alert rules display

4. **Agent Health Summary**
   - [ ] Healthy/Unhealthy/Restarting counts
   - [ ] Last restart times
   - [ ] Error rate per agent
   - [ ] "Restart All" emergency action

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `AgentLoadBalancer.test.jsx` | Tree renders, scale actions work |
| `ProcessTree.test.jsx` | PID display, expand/collapse |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/architect/system`

**Macro Task:** The Architect

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

