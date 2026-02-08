# Phase 2 Implementation Plan: Monitoring & Observability Suite

> **Phase**: 2 of 33  
> **Status**: ✅ Completed  
> **Priority**: CRITICAL  
> **Estimated Duration**: 4 days  
> **Dependencies**: Phase 1 (Infrastructure base)

---

## Overview

Phase 2 builds the observability layer enabling proactive system monitoring. This phase creates service health dashboards, latency tracking, WebSocket connection management, middleware pipeline visualization, and alert configuration interfaces.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `monitoring` | `services/monitoring/` | `health_check.py`, `latency_tracker.py`, `alert_rules.py` |
| `streaming` | `services/streaming/` | `websocket_manager.py`, `connection_pool.py` |
| `middleware` | `services/middleware/` | `pipeline.py`, `interceptors.py` |

---

## Deliverable 1: Service Health Grid Page
> **Status**: ✅ Completed

### 1.1 Description
Full-page interface (`/admin/health`) displaying all-services status grid with uptime history, health check results, and dependency mapping.

### 1.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `ServiceHealthGrid.jsx` | `frontend/src/pages/admin/ServiceHealthGrid.jsx` | Page |
| `ServiceCard.jsx` | `frontend/src/components/cards/ServiceCard.jsx` | Card |
| `UptimeSparkline.jsx` | `frontend/src/components/charts/UptimeSparkline.jsx` | Chart |
| `DependencyGraph.jsx` | `frontend/src/components/admin/DependencyGraph.jsx` | Widget |
| `HealthCheckModal.jsx` | `frontend/src/components/modals/HealthCheckModal.jsx` | Modal |

### 1.3 Backend Implementation

| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/api/v1/admin/health/services` | `list_services()` | All services with health status |
| GET | `/api/v1/admin/health/services/{service_id}` | `get_service_health()` | Detailed service health |
| GET | `/api/v1/admin/health/services/{service_id}/history` | `get_uptime_history()` | 30-day uptime history |
| POST | `/api/v1/admin/health/services/{service_id}/check` | `trigger_health_check()` | Manual health check |
| GET | `/api/v1/admin/health/dependencies` | `get_dependency_map()` | Service dependency graph |

### 1.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F2.1.1**: Grid displays all services with color-coded status (green/yellow/red)
- [ ] **F2.1.2**: Click service card shows 30-day uptime sparkline
- [ ] **F2.1.3**: Dependency graph shows service connections with health propagation
- [ ] **F2.1.4**: Manual health check button triggers immediate check
- [ ] **F2.1.5**: Auto-refresh every 30 seconds with last-updated timestamp

#### Integration Requirements
- [ ] **I2.1.1**: Page fetches `GET /api/v1/admin/health/services` on mount
- [ ] **I2.1.2**: Card expansion loads history from `GET .../history`
- [ ] **I2.1.3**: Health check POST returns within 5 seconds
- [ ] **I2.1.4**: Failed services bubble to top of grid

#### Response Handling
- [ ] **R2.1.1**: Service schema: `{ id, name, status, last_check, uptime_pct, dependencies[] }`
- [ ] **R2.1.2**: 503 status shown when monitoring service itself is down
- [ ] **R2.1.3**: Partial failures show degraded status with affected components

---

## Deliverable 2: Latency Heatmap Widget
> **Status**: ✅ Completed

### 2.1 Description
Widget displaying P50/P95/P99 latencies across all API endpoints, with drill-down capability to individual endpoint histograms.

### 2.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `LatencyHeatmapWidget.jsx` | `frontend/src/components/widgets/LatencyHeatmapWidget.jsx` | Widget |
| `EndpointLatencyRow.jsx` | `frontend/src/components/admin/EndpointLatencyRow.jsx` | Row |
| `LatencyHistogram.jsx` | `frontend/src/components/charts/LatencyHistogram.jsx` | Chart |
| `LatencyTrendChart.jsx` | `frontend/src/components/charts/LatencyTrendChart.jsx` | Chart |

### 2.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/latency/summary` | `get_latency_summary()` |
| GET | `/api/v1/admin/latency/endpoints` | `list_endpoint_latencies()` |
| GET | `/api/v1/admin/latency/endpoints/{path}/histogram` | `get_endpoint_histogram()` |
| GET | `/api/v1/admin/latency/endpoints/{path}/trend` | `get_latency_trend()` |

### 2.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F2.2.1**: Heatmap shows P50/P95/P99 for top 20 endpoints by traffic
- [ ] **F2.2.2**: Color scale: green (<100ms), yellow (100-500ms), red (>500ms)
- [ ] **F2.2.3**: Click endpoint row shows histogram of response times
- [ ] **F2.2.4**: Trend chart shows 24-hour latency evolution
- [ ] **F2.2.5**: Sort by P99, P95, P50, or request count

#### Integration Requirements
- [ ] **I2.2.1**: Widget fetches summary on mount, updates every 60 seconds
- [ ] **I2.2.2**: Histogram data includes bucket counts for distribution
- [ ] **I2.2.3**: Trend data includes hourly aggregates

#### Response Handling
- [ ] **R2.2.1**: Summary schema: `{ endpoints: [{ path, method, p50, p95, p99, count }] }`
- [ ] **R2.2.2**: Histogram schema: `{ buckets: [{ range, count }] }`
- [ ] **R2.2.3**: Empty data shows "Insufficient data" message

---

## Deliverable 3: WebSocket Status Widget
> **Status**: ✅ Completed

### 3.1 Description
Widget showing active WebSocket connections, message rates, errors, and connection pool health.

### 3.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `WebSocketStatusWidget.jsx` | `frontend/src/components/widgets/WebSocketStatusWidget.jsx` | Widget |
| `ConnectionPoolMeter.jsx` | `frontend/src/components/charts/ConnectionPoolMeter.jsx` | Chart |
| `MessageRateChart.jsx` | `frontend/src/components/charts/MessageRateChart.jsx` | Chart |
| `ConnectionListPanel.jsx` | `frontend/src/components/panels/ConnectionListPanel.jsx` | Panel |

### 3.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/websocket/stats` | `get_websocket_stats()` |
| GET | `/api/v1/admin/websocket/connections` | `list_active_connections()` |
| POST | `/api/v1/admin/websocket/connections/{conn_id}/disconnect` | `force_disconnect()` |
| GET | `/api/v1/admin/websocket/errors` | `get_recent_errors()` |

### 3.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F2.3.1**: Pool meter shows active/max connections with percentage
- [ ] **F2.3.2**: Message rate chart shows messages/second (sent/received)
- [ ] **F2.3.3**: Connection list shows client IP, connected duration, subscriptions
- [ ] **F2.3.4**: Force disconnect button terminates specific connections
- [ ] **F2.3.5**: Error panel shows last 20 WebSocket errors

#### Integration Requirements
- [ ] **I2.3.1**: Stats endpoint polled every 5 seconds
- [ ] **I2.3.2**: Force disconnect requires admin role confirmation
- [ ] **I2.3.3**: Real-time updates via WebSocket subscription

#### Response Handling
- [ ] **R2.3.1**: Stats schema: `{ active, max, msg_in_rate, msg_out_rate, error_rate }`
- [ ] **R2.3.2**: Connection schema: `{ id, client_ip, connected_at, subscriptions[] }`
- [ ] **R2.3.3**: 403 Forbidden if user lacks admin role

---

## Deliverable 4: Middleware Pipeline Page
> **Status**: ✅ Completed

### 4.1 Description
Page (`/admin/middleware`) visualizing the request/response interceptor chain, allowing reordering and toggling of middleware components.

### 4.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `MiddlewarePipeline.jsx` | `frontend/src/pages/admin/MiddlewarePipeline.jsx` | Page |
| `MiddlewareStep.jsx` | `frontend/src/components/admin/MiddlewareStep.jsx` | Card |
| `PipelineFlowChart.jsx` | `frontend/src/components/admin/PipelineFlowChart.jsx` | Chart |
| `MiddlewareConfigModal.jsx` | `frontend/src/components/modals/MiddlewareConfigModal.jsx` | Modal |

### 4.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/middleware/pipeline` | `get_pipeline_config()` |
| PUT | `/api/v1/admin/middleware/pipeline` | `update_pipeline_order()` |
| GET | `/api/v1/admin/middleware/{middleware_id}` | `get_middleware_details()` |
| PATCH | `/api/v1/admin/middleware/{middleware_id}` | `toggle_middleware()` |
| GET | `/api/v1/admin/middleware/stats` | `get_middleware_stats()` |

### 4.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F2.4.1**: Flow chart shows request → middleware1 → middleware2 → ... → handler
- [ ] **F2.4.2**: Drag-and-drop reordering of middleware steps
- [ ] **F2.4.3**: Toggle switch enables/disables individual middleware
- [ ] **F2.4.4**: Stats show avg processing time per middleware
- [ ] **F2.4.5**: Config modal edits middleware-specific settings

#### Integration Requirements
- [ ] **I2.4.1**: Pipeline config loaded on page mount
- [ ] **I2.4.2**: Reorder saves via PUT with new order array
- [ ] **I2.4.3**: Toggle uses PATCH with `{ enabled: boolean }`
- [ ] **I2.4.4**: Changes require server restart notice

#### Response Handling
- [ ] **R2.4.1**: Pipeline schema: `{ steps: [{ id, name, order, enabled, avg_ms }] }`
- [ ] **R2.4.2**: 409 Conflict if pipeline state changed since load
- [ ] **R2.4.3**: Success shows "Restart required" warning

---

## Deliverable 5: Alert Configuration Page
> **Status**: ✅ Completed

### 5.1 Description
Page (`/admin/alerts-config`) for configuring thresholds, notification channels, and escalation rules for system alerts.

### 5.2 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `AlertConfigPage.jsx` | `frontend/src/pages/admin/AlertConfigPage.jsx` | Page |
| `AlertRuleCard.jsx` | `frontend/src/components/cards/AlertRuleCard.jsx` | Card |
| `AlertRuleEditor.jsx` | `frontend/src/components/admin/AlertRuleEditor.jsx` | Form |
| `NotificationChannelConfig.jsx` | `frontend/src/components/admin/NotificationChannelConfig.jsx` | Widget |
| `AlertPreviewModal.jsx` | `frontend/src/components/modals/AlertPreviewModal.jsx` | Modal |

### 5.3 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/admin/alerts/rules` | `list_alert_rules()` |
| POST | `/api/v1/admin/alerts/rules` | `create_alert_rule()` |
| PUT | `/api/v1/admin/alerts/rules/{rule_id}` | `update_alert_rule()` |
| DELETE | `/api/v1/admin/alerts/rules/{rule_id}` | `delete_alert_rule()` |
| GET | `/api/v1/admin/alerts/channels` | `list_notification_channels()` |
| POST | `/api/v1/admin/alerts/rules/{rule_id}/test` | `test_alert_rule()` |

### 5.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F2.5.1**: List all alert rules with status (active/paused)
- [ ] **F2.5.2**: Create rule with metric, threshold, operator, duration
- [ ] **F2.5.3**: Configure notification channels (Slack, email, SMS)
- [ ] **F2.5.4**: Test rule sends sample notification to selected channel
- [ ] **F2.5.5**: Rule preview shows last 24h of metric with threshold line

#### Integration Requirements
- [ ] **I2.5.1**: Rule CRUD follows standard REST patterns
- [ ] **I2.5.2**: Test POST returns send result within 10 seconds
- [ ] **I2.5.3**: Channel config includes webhook URLs, email addresses
- [ ] **I2.5.4**: Validation errors show field-level feedback

#### Response Handling
- [ ] **R2.5.1**: Rule schema: `{ id, name, metric, operator, threshold, duration, channels[], enabled }`
- [ ] **R2.5.2**: 422 Unprocessable Entity for invalid rule definitions
- [ ] **R2.5.3**: Test result schema: `{ success, channel, message?, error? }`

---

## Testing Requirements

### Unit Tests
| Component | Test File | Coverage Target |
|-----------|-----------|-----------------|
| ServiceHealthGrid | `tests/frontend/admin/ServiceHealthGrid.test.jsx` | 80% |
| LatencyHeatmapWidget | `tests/frontend/widgets/LatencyHeatmapWidget.test.jsx` | 80% |
| health_api | `tests/backend/api/test_health_api.py` | 90% |
| latency_api | `tests/backend/api/test_latency_api.py` | 90% |

### Integration Tests
| Test Suite | Description |
|------------|-------------|
| `test_phase2_health_e2e.py` | Service grid → health check → dependency view |
| `test_phase2_latency_e2e.py` | Heatmap → endpoint drill-down → histogram |
| `test_phase2_websocket_e2e.py` | Stats → connection list → force disconnect |
| `test_phase2_alerts_e2e.py` | Create rule → test → verify notification |

---

## Deployment Checklist

- [ ] All API endpoints registered in gateway
- [ ] Frontend routes added to router
- [ ] Admin menu navigation updated
- [ ] Prometheus metrics exported for new endpoints
- [ ] Grafana dashboards created
- [ ] Alert channel integrations tested
- [ ] Documentation updated

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 2 Implementation Plan - Version 1.0*
