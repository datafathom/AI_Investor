# Phase 1 Implementation Plan: Infrastructure Monitoring Dashboard

> **Phase**: 1 of 33  
> **Status**: 🔴 Not Started  
> **Priority**: CRITICAL  
> **Estimated Duration**: 5 days  
> **Dependencies**: None (Foundation Phase)

---

## Overview

Phase 1 establishes the foundational infrastructure monitoring capabilities for the Sovereign OS. This phase creates visibility into the core event bus, caching layer, Kafka consumers, private cloud storage, Neo4j graph database, and system logging. Without these monitoring interfaces, operators cannot diagnose system health or troubleshoot issues.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `infrastructure` | `services/infrastructure/` | `event_bus.py`, `cache_service.py`, `private_cloud.py` |
| `kafka` | `services/kafka/` | `consumer.py`, `orderbook_consumer.py`, `graph_bridge.py` |
| `neo4j` | `services/neo4j/` | `graph_manager.py`, `query_service.py` |
| `caching` | `services/caching/` | `redis_cache.py`, `memory_cache.py` |
| `logging` | `services/logging/` | `log_service.py`, `log_aggregator.py` |
| `system` | `services/system/` | `env_manager.py`, `health_check.py` |

---

## Deliverable 1: Event Bus Monitor Page

### 1.1 Description
A dedicated full-page interface (`/admin/event-bus`) that visualizes real-time pub/sub message flow across all system topics. Operators can see message throughput, topic subscriptions, and replay failed messages.

### 1.2 Frontend Implementation

#### Components to Create
| Component | Path | Type | Description |
|-----------|------|------|-------------|
| `EventBusMonitor.jsx` | `frontend/src/pages/admin/EventBusMonitor.jsx` | Page | Main page component |
| `TopicList.jsx` | `frontend/src/components/admin/TopicList.jsx` | Widget | List of active topics with subscriber counts |
| `MessageFlowChart.jsx` | `frontend/src/components/admin/MessageFlowChart.jsx` | Widget | Real-time line chart of message throughput |
| `MessageInspector.jsx` | `frontend/src/components/admin/MessageInspector.jsx` | Panel | Side panel to inspect individual messages |
| `TopicSubscriptionModal.jsx` | `frontend/src/components/admin/TopicSubscriptionModal.jsx` | Modal | Subscribe/unsubscribe from topics |

#### UI/UX Requirements
- [ ] Topic list displays all registered topics with color-coded activity status
- [ ] Message flow chart updates every 5 seconds with configurable refresh rate
- [ ] Click on topic to filter message inspector to that topic only
- [ ] Dark mode support with "Heavy/Industrial" design language
- [ ] Responsive layout: 3-column on desktop, stacked on tablet/mobile

### 1.3 Backend Implementation

#### API Endpoints to Create
| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/api/v1/admin/event-bus/topics` | `get_all_topics()` | List all topics with metadata |
| GET | `/api/v1/admin/event-bus/topics/{topic}/messages` | `get_topic_messages()` | Recent messages for a topic (paginated) |
| GET | `/api/v1/admin/event-bus/stats` | `get_event_bus_stats()` | Throughput metrics per topic |
| POST | `/api/v1/admin/event-bus/topics/{topic}/replay` | `replay_message()` | Replay a specific message |
| WS | `/ws/admin/event-bus/stream` | `stream_events()` | Real-time WebSocket event stream |

#### Backend Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| `web/api/admin/event_bus_api.py` | CREATE | FastAPI router for event bus endpoints |
| `services/infrastructure/event_bus.py` | MODIFY | Add `get_stats()`, `get_recent_messages()` methods |
| `web/websocket/event_bus_ws.py` | CREATE | WebSocket handler for live streaming |

### 1.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F1.1.1**: Page loads within 2 seconds and displays all active topics
- [ ] **F1.1.2**: Real-time chart updates without page refresh (WebSocket)
- [ ] **F1.1.3**: Clicking a topic filters the message inspector to show only that topic's messages
- [ ] **F1.1.4**: Replay button resends the selected message to its original topic
- [ ] **F1.1.5**: Pagination loads next 50 messages when scrolling message inspector

#### Integration Requirements
- [ ] **I1.1.1**: Frontend service calls `GET /api/v1/admin/event-bus/topics` on page mount
- [ ] **I1.1.2**: WebSocket connection established to `/ws/admin/event-bus/stream` for live updates
- [ ] **I1.1.3**: Error states display user-friendly messages with retry buttons
- [ ] **I1.1.4**: Loading skeletons shown while data is being fetched

#### Response Handling
- [ ] **R1.1.1**: 200 OK responses populate the UI with topic/message data
- [ ] **R1.1.2**: 401 Unauthorized redirects to login page
- [ ] **R1.1.3**: 500 Server Error shows toast notification with error details
- [ ] **R1.1.4**: WebSocket disconnection triggers auto-reconnect with exponential backoff

---

## Deliverable 2: Cache Analytics Widget

### 2.1 Description
A reusable widget component that displays cache hit/miss ratios, memory usage, and provides cache invalidation controls. This widget is embedded in Mission Control and the Admin Settings panel.

### 2.2 Frontend Implementation

#### Components to Create
| Component | Path | Type | Description |
|-----------|------|------|-------------|
| `CacheAnalyticsWidget.jsx` | `frontend/src/components/widgets/CacheAnalyticsWidget.jsx` | Widget | Main widget component |
| `CacheHitMissChart.jsx` | `frontend/src/components/charts/CacheHitMissChart.jsx` | Chart | Donut chart showing hit/miss ratio |
| `CacheMemoryBar.jsx` | `frontend/src/components/charts/CacheMemoryBar.jsx` | Chart | Progress bar for memory usage |
| `CacheInvalidateModal.jsx` | `frontend/src/components/modals/CacheInvalidateModal.jsx` | Modal | Confirm cache invalidation |

#### UI/UX Requirements
- [ ] Widget header shows cache name and overall health status
- [ ] Donut chart animates on load and updates on refresh
- [ ] Memory bar changes color: green (<70%), yellow (70-90%), red (>90%)
- [ ] Invalidate button requires confirmation modal with pattern input
- [ ] Tooltip on hover shows exact numbers and timestamps

### 2.3 Backend Implementation

#### API Endpoints to Create
| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/api/v1/admin/cache/stats` | `get_cache_stats()` | Aggregate cache statistics |
| GET | `/api/v1/admin/cache/{cache_name}/stats` | `get_specific_cache_stats()` | Stats for specific cache |
| POST | `/api/v1/admin/cache/{cache_name}/invalidate` | `invalidate_cache()` | Invalidate cache entries by pattern |
| GET | `/api/v1/admin/cache/{cache_name}/keys` | `list_cache_keys()` | List cached keys (paginated) |

#### Backend Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| `web/api/admin/cache_api.py` | CREATE | FastAPI router for cache endpoints |
| `services/infrastructure/cache_service.py` | MODIFY | Add `get_stats()`, `invalidate_pattern()` methods |
| `services/caching/redis_cache.py` | MODIFY | Add `memory_usage()`, `key_count()` methods |

### 2.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F1.2.1**: Widget displays hit rate percentage with 2 decimal precision
- [ ] **F1.2.2**: Memory usage shows current/max with percentage
- [ ] **F1.2.3**: 24-hour trend chart shows hourly hit/miss averages
- [ ] **F1.2.4**: Cache invalidation with pattern `user:*` clears all user-prefixed keys
- [ ] **F1.2.5**: Key browser allows searching and viewing individual cached values

#### Integration Requirements
- [ ] **I1.2.1**: Widget fetches data from `GET /api/v1/admin/cache/stats` on mount
- [ ] **I1.2.2**: Refresh button triggers immediate data reload
- [ ] **I1.2.3**: Invalidation POST returns count of invalidated keys
- [ ] **I1.2.4**: Widget re-fetches stats after successful invalidation

#### Response Handling
- [ ] **R1.2.1**: Stats response schema: `{ hit_rate, miss_rate, memory_used_mb, memory_max_mb, key_count }`
- [ ] **R1.2.2**: Invalidation success shows toast: "Invalidated {n} keys"
- [ ] **R1.2.3**: Redis connection failure shows "Cache Unavailable" state with reconnect option

---

## Deliverable 3: Kafka Consumer Health Widget

### 3.1 Description
A widget displaying the health status of all Kafka consumers, including consumer lag, partition offsets, and throughput metrics. Embedded in Mission Control.

### 3.2 Frontend Implementation

#### Components to Create
| Component | Path | Type | Description |
|-----------|------|------|-------------|
| `KafkaHealthWidget.jsx` | `frontend/src/components/widgets/KafkaHealthWidget.jsx` | Widget | Main widget component |
| `ConsumerGroupCard.jsx` | `frontend/src/components/cards/ConsumerGroupCard.jsx` | Card | Individual consumer group status |
| `PartitionLagChart.jsx` | `frontend/src/components/charts/PartitionLagChart.jsx` | Chart | Bar chart showing lag per partition |
| `ConsumerDetailsPanel.jsx` | `frontend/src/components/panels/ConsumerDetailsPanel.jsx` | Panel | Detailed consumer group info |

#### UI/UX Requirements
- [ ] Consumer groups displayed as cards with status indicators (●)
- [ ] Green: lag < 100, Yellow: lag 100-1000, Red: lag > 1000
- [ ] Click on card expands to show partition-level details
- [ ] Auto-refresh every 10 seconds with manual refresh option
- [ ] Connection status indicator in widget header

### 3.3 Backend Implementation

#### API Endpoints to Create
| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/api/v1/admin/kafka/consumers` | `list_consumer_groups()` | List all consumer groups |
| GET | `/api/v1/admin/kafka/consumers/{group_id}` | `get_consumer_group_details()` | Detailed group info with partitions |
| GET | `/api/v1/admin/kafka/consumers/{group_id}/lag` | `get_consumer_lag()` | Lag metrics per partition |
| POST | `/api/v1/admin/kafka/consumers/{group_id}/reset` | `reset_consumer_offsets()` | Reset offsets to earliest/latest |

#### Backend Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| `web/api/admin/kafka_api.py` | CREATE | FastAPI router for Kafka endpoints |
| `services/kafka/consumer.py` | MODIFY | Add `get_lag_metrics()`, `list_groups()` methods |
| `services/kafka/admin_client.py` | CREATE | Kafka AdminClient wrapper for offset management |

### 3.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F1.3.1**: All consumer groups listed with current offset and end offset
- [ ] **F1.3.2**: Lag calculated as (end_offset - current_offset) per partition
- [ ] **F1.3.3**: Throughput shows messages/second over last 5 minutes
- [ ] **F1.3.4**: Offset reset requires confirmation with timestamp/offset input
- [ ] **F1.3.5**: Dead consumers (no heartbeat > 30s) show warning badge

#### Integration Requirements
- [ ] **I1.3.1**: Frontend polls `GET /api/v1/admin/kafka/consumers` every 10 seconds
- [ ] **I1.3.2**: Expanding a card loads detailed data via `GET .../consumers/{group_id}`
- [ ] **I1.3.3**: Reset offset POST includes `{ strategy: 'earliest' | 'latest' | 'timestamp', value?: number }`

#### Response Handling
- [ ] **R1.3.1**: Consumer list schema: `[{ group_id, state, members, total_lag }]`
- [ ] **R1.3.2**: Kafka broker unreachable returns 503 with "Kafka Unavailable" UI state
- [ ] **R1.3.3**: Successful offset reset shows toast with new offset positions

---

## Deliverable 4: Private Cloud Storage Page

### 4.1 Description
A full-page interface (`/admin/storage`) for managing the platform's private cloud storage (ZFS pools, Nextcloud sync). Displays quota usage, pool health, and sync status.

### 4.2 Frontend Implementation

#### Components to Create
| Component | Path | Type | Description |
|-----------|------|------|-------------|
| `StorageManager.jsx` | `frontend/src/pages/admin/StorageManager.jsx` | Page | Main page component |
| `StoragePoolCard.jsx` | `frontend/src/components/cards/StoragePoolCard.jsx` | Card | Individual ZFS pool status |
| `StorageQuotaRing.jsx` | `frontend/src/components/charts/StorageQuotaRing.jsx` | Chart | Circular quota visualization |
| `SyncStatusTimeline.jsx` | `frontend/src/components/admin/SyncStatusTimeline.jsx` | Widget | Recent sync operations timeline |
| `UploadModal.jsx` | `frontend/src/components/modals/UploadModal.jsx` | Modal | Manual file upload interface |

#### UI/UX Requirements
- [ ] Pool cards show name, used/total, health status, redundancy level
- [ ] Quota rings are color-coded by usage percentage
- [ ] Sync timeline shows last 20 operations with status icons
- [ ] Drag-and-drop file upload to designated pools
- [ ] Storage alerts banner for pools > 85% usage

### 4.3 Backend Implementation

#### API Endpoints to Create
| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/api/v1/admin/storage/pools` | `list_storage_pools()` | List all ZFS pools |
| GET | `/api/v1/admin/storage/pools/{pool_id}` | `get_pool_details()` | Detailed pool info |
| GET | `/api/v1/admin/storage/sync/history` | `get_sync_history()` | Recent sync operations |
| POST | `/api/v1/admin/storage/sync/trigger` | `trigger_sync()` | Manually trigger Nextcloud sync |
| POST | `/api/v1/admin/storage/upload` | `upload_file()` | Upload file to specified pool |
| GET | `/api/v1/admin/storage/quota` | `get_quota_status()` | Overall quota across pools |

#### Backend Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| `web/api/admin/storage_api.py` | CREATE | FastAPI router for storage endpoints |
| `services/infrastructure/private_cloud.py` | MODIFY | Add `list_pools()`, `trigger_sync()`, `upload()` methods |
| `services/storage/zfs_manager.py` | CREATE | ZFS pool management via subprocess |

### 4.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F1.4.1**: All ZFS pools displayed with RAID level and health (ONLINE/DEGRADED/FAULTED)
- [ ] **F1.4.2**: Quota ring shows used/available with TB precision
- [ ] **F1.4.3**: Sync history shows timestamps, file counts, and success/failure status
- [ ] **F1.4.4**: Manual sync button triggers immediate sync with progress indicator
- [ ] **F1.4.5**: File upload supports drag-and-drop with progress bar

#### Integration Requirements
- [ ] **I1.4.1**: Page loads pool data from `GET /api/v1/admin/storage/pools` on mount
- [ ] **I1.4.2**: File upload uses multipart/form-data POST to `/api/v1/admin/storage/upload`
- [ ] **I1.4.3**: Sync trigger returns job ID for status polling
- [ ] **I1.4.4**: Toast notifications for sync completion (success/failure)

#### Response Handling
- [ ] **R1.4.1**: Pool schema: `{ pool_id, name, size_tb, used_tb, health, redundancy, scrub_status }`
- [ ] **R1.4.2**: Upload progress reported via chunked transfer with percentage
- [ ] **R1.4.3**: 507 Insufficient Storage when pool is > 95% full
- [ ] **R1.4.4**: Degraded pool triggers warning banner with disk replacement guidance

---

## Deliverable 5: Neo4j Graph Browser Page

### 5.1 Description
A full-page interface (`/admin/graph-browser`) for exploring the Neo4j knowledge graph. Supports Cypher query execution, visual node/edge exploration, and relationship path finding.

### 5.2 Frontend Implementation

#### Components to Create
| Component | Path | Type | Description |
|-----------|------|------|-------------|
| `GraphBrowser.jsx` | `frontend/src/pages/admin/GraphBrowser.jsx` | Page | Main page component |
| `CypherConsole.jsx` | `frontend/src/components/admin/CypherConsole.jsx` | Widget | Query input with syntax highlighting |
| `GraphCanvas.jsx` | `frontend/src/components/admin/GraphCanvas.jsx` | Widget | Force-directed graph visualization |
| `NodeInspector.jsx` | `frontend/src/components/panels/NodeInspector.jsx` | Panel | Selected node properties panel |
| `QueryHistoryDrawer.jsx` | `frontend/src/components/admin/QueryHistoryDrawer.jsx` | Drawer | Recent queries with replay |

#### UI/UX Requirements
- [ ] Cypher console with syntax highlighting (CodeMirror or Monaco)
- [ ] Graph canvas uses D3.js force-directed layout with zoom/pan
- [ ] Node colors based on label (Account=blue, Transaction=green, etc.)
- [ ] Click node to select and show properties in inspector
- [ ] Double-click node to expand its relationships
- [ ] Query history persisted to localStorage

### 5.3 Backend Implementation

#### API Endpoints to Create
| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| POST | `/api/v1/admin/graph/query` | `execute_cypher()` | Execute Cypher query |
| GET | `/api/v1/admin/graph/node/{node_id}` | `get_node_details()` | Get node properties |
| GET | `/api/v1/admin/graph/node/{node_id}/neighbors` | `get_node_neighbors()` | Get connected nodes |
| GET | `/api/v1/admin/graph/stats` | `get_graph_stats()` | Node/edge counts by label |
| GET | `/api/v1/admin/graph/schema` | `get_graph_schema()` | Labels, relationship types, property keys |

#### Backend Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| `web/api/admin/graph_api.py` | CREATE | FastAPI router for graph endpoints |
| `services/neo4j/graph_manager.py` | MODIFY | Add `execute_query()`, `get_schema()` methods |
| `services/neo4j/query_sanitizer.py` | CREATE | Cypher injection prevention |

### 5.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F1.5.1**: Cypher queries execute and return results within 5 seconds (timeout configurable)
- [ ] **F1.5.2**: Graph visualization renders up to 500 nodes smoothly
- [ ] **F1.5.3**: Node inspector shows all properties with type indicators
- [ ] **F1.5.4**: Relationship expansion loads neighbors without full page reload
- [ ] **F1.5.5**: Query history stores last 50 queries with execution time

#### Integration Requirements
- [ ] **I1.5.1**: Query submission via POST with body `{ cypher: string, params?: object }`
- [ ] **I1.5.2**: Response includes `nodes` and `relationships` arrays for visualization
- [ ] **I1.5.3**: Schema endpoint used to populate autocomplete in Cypher console
- [ ] **I1.5.4**: Query cancellation supported via AbortController

#### Response Handling
- [ ] **R1.5.1**: Query results schema: `{ nodes: [], relationships: [], stats: { nodesCreated, ... } }`
- [ ] **R1.5.2**: Syntax errors return 400 with error position for highlighting
- [ ] **R1.5.3**: 504 Gateway Timeout for queries exceeding time limit
- [ ] **R1.5.4**: Write queries disabled in read-only mode (configurable)

---

## Deliverable 6: System Logs Viewer Page

### 6.1 Description
A full-page interface (`/admin/logs`) for viewing, searching, and filtering aggregated system logs. Supports log level filtering, text search, and time range selection.

### 6.2 Frontend Implementation

#### Components to Create
| Component | Path | Type | Description |
|-----------|------|------|-------------|
| `LogViewer.jsx` | `frontend/src/pages/admin/LogViewer.jsx` | Page | Main page component |
| `LogFilterBar.jsx` | `frontend/src/components/admin/LogFilterBar.jsx` | Widget | Level, service, time range filters |
| `LogTable.jsx` | `frontend/src/components/admin/LogTable.jsx` | Widget | Virtualized log table |
| `LogDetailModal.jsx` | `frontend/src/components/modals/LogDetailModal.jsx` | Modal | Full log entry with stack trace |
| `LogExportButton.jsx` | `frontend/src/components/buttons/LogExportButton.jsx` | Button | Export filtered logs to CSV/JSON |

#### UI/UX Requirements
- [ ] Log levels color-coded: DEBUG (gray), INFO (blue), WARN (yellow), ERROR (red), CRITICAL (purple)
- [ ] Virtualized scrolling for performance (10k+ rows)
- [ ] Full-text search with highlight matching
- [ ] Time range picker with presets (1h, 24h, 7d, custom)
- [ ] Live tail mode with auto-scroll

### 6.3 Backend Implementation

#### API Endpoints to Create
| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/api/v1/admin/logs` | `get_logs()` | Filtered, paginated logs |
| GET | `/api/v1/admin/logs/{log_id}` | `get_log_detail()` | Full log entry with context |
| GET | `/api/v1/admin/logs/services` | `list_log_services()` | Available services for filtering |
| GET | `/api/v1/admin/logs/export` | `export_logs()` | Export logs as CSV/JSON |
| WS | `/ws/admin/logs/tail` | `tail_logs()` | Real-time log streaming |

#### Backend Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| `web/api/admin/logs_api.py` | CREATE | FastAPI router for log endpoints |
| `services/logging/log_service.py` | MODIFY | Add `search()`, `export()` methods |
| `web/websocket/log_tail_ws.py` | CREATE | WebSocket handler for log tailing |

### 6.4 End-to-End Acceptance Criteria

#### Functional Requirements
- [ ] **F1.6.1**: Logs load with pagination (100 per page default)
- [ ] **F1.6.2**: Filter by level, service, and time range simultaneously
- [ ] **F1.6.3**: Search highlights matching text in log messages
- [ ] **F1.6.4**: Click log row opens detail modal with full stack trace
- [ ] **F1.6.5**: Export generates downloadable file within 10 seconds (up to 10k rows)

#### Integration Requirements
- [ ] **I1.6.1**: Log query params: `?level=ERROR&service=trading&from=2026-02-01&to=2026-02-08&search=timeout`
- [ ] **I1.6.2**: WebSocket connection for live tail mode with filter subscription
- [ ] **I1.6.3**: Cursor-based pagination for efficient deep scrolling
- [ ] **I1.6.4**: Export endpoint streams file with Content-Disposition header

#### Response Handling
- [ ] **R1.6.1**: Log entry schema: `{ id, timestamp, level, service, message, stacktrace?, metadata? }`
- [ ] **R1.6.2**: Empty results show "No logs matching filters" message
- [ ] **R1.6.3**: Large exports (>10k) return 413 with suggestion to narrow filters
- [ ] **R1.6.4**: WebSocket reconnects automatically on network interruption

---

## Testing Requirements

### Unit Tests
| Component | Test File | Coverage Target |
|-----------|-----------|-----------------|
| EventBusMonitor | `tests/frontend/admin/EventBusMonitor.test.jsx` | 80% |
| CacheAnalyticsWidget | `tests/frontend/widgets/CacheAnalyticsWidget.test.jsx` | 80% |
| KafkaHealthWidget | `tests/frontend/widgets/KafkaHealthWidget.test.jsx` | 80% |
| event_bus_api | `tests/backend/api/test_event_bus_api.py` | 90% |
| cache_api | `tests/backend/api/test_cache_api.py` | 90% |
| kafka_api | `tests/backend/api/test_kafka_api.py` | 90% |

### Integration Tests
| Test Suite | Description |
|------------|-------------|
| `test_phase1_event_bus_e2e.py` | Full page load → filter → message replay |
| `test_phase1_cache_e2e.py` | Widget load → invalidate → verify cleared |
| `test_phase1_kafka_e2e.py` | Consumer list → group detail → offset reset |
| `test_phase1_storage_e2e.py` | Pool list → upload → sync → verify |
| `test_phase1_graph_e2e.py` | Query execution → visualization → node inspect |
| `test_phase1_logs_e2e.py` | Load → filter → search → export |

---

## Deployment Checklist

- [ ] All API endpoints added to `web/fastapi_gateway.py` router registry
- [ ] WebSocket handlers registered in gateway
- [ ] Frontend routes added to `frontend/src/App.jsx`
- [ ] Admin navigation menu updated with new pages
- [ ] Environment variables documented in `.env.template`
- [ ] Database migrations (if any) applied
- [ ] Feature flags configured for gradual rollout
- [ ] Monitoring dashboards created for new endpoints
- [ ] Documentation updated in `docs/admin/`

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 1 Implementation Plan - Version 1.0*
