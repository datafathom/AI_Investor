# Phase 5 Implementation Plan: Data Ingestion & Integration

> **Phase**: 5 of 33  
> **Status**: 🔴 Not Started  
> **Priority**: HIGH  
> **Estimated Duration**: 5 days  
> **Dependencies**: Phase 4 (Market Data Foundation)

---

## Overview

Phase 5 builds the data ingestion infrastructure including ETL pipeline management, third-party API connectors, external data source configuration, webhook receivers, and data quality monitoring.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `ingestion` | `services/ingestion/` | `pipeline_manager.py`, `quality_checker.py` |
| `integration` | `services/integration/` | `webhook_handler.py`, `sync_service.py` |
| `integrations` | `services/integrations/` | `connector_registry.py`, `oauth_manager.py` |
| `external` | `services/external/` | `data_sources.py`, `provider_health.py` |

---

## Deliverable 1: Data Pipeline Manager Page

### 1.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `DataPipelineManager.jsx` | `frontend/src/pages/admin/DataPipelineManager.jsx` | Page |
| `PipelineDAG.jsx` | `frontend/src/components/charts/PipelineDAG.jsx` | Chart |
| `PipelineStatusCard.jsx` | `frontend/src/components/cards/PipelineStatusCard.jsx` | Card |
| `JobDetailPanel.jsx` | `frontend/src/components/panels/JobDetailPanel.jsx` | Panel |
| `TriggerPipelineModal.jsx` | `frontend/src/components/modals/TriggerPipelineModal.jsx` | Modal |

### 1.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/ingestion/pipelines` | `list_pipelines()` |
| GET | `/api/v1/ingestion/pipelines/{id}` | `get_pipeline_details()` |
| POST | `/api/v1/ingestion/pipelines/{id}/trigger` | `trigger_pipeline()` |
| GET | `/api/v1/ingestion/pipelines/{id}/runs` | `get_pipeline_runs()` |
| PATCH | `/api/v1/ingestion/pipelines/{id}` | `update_pipeline_config()` |

### 1.3 End-to-End Acceptance Criteria

- [ ] **F5.1.1**: DAG shows ETL dependencies with status colors
- [ ] **F5.1.2**: Click node shows job details, last run, duration
- [ ] **F5.1.3**: Manual trigger executes pipeline with optional params
- [ ] **F5.1.4**: Run history shows success/failure with retry counts
- [ ] **F5.1.5**: Config edit updates schedule, parallelism, retries
- [ ] **I5.1.1**: Trigger POST returns run ID for status polling
- [ ] **I5.1.2**: WebSocket updates job status in real-time
- [ ] **R5.1.1**: Pipeline schema: `{ id, name, schedule, status, jobs[] }`
- [ ] **R5.1.2**: 409 Conflict if pipeline already running

---

## Deliverable 2: API Connector Hub Page

### 2.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `APIConnectorHub.jsx` | `frontend/src/pages/admin/APIConnectorHub.jsx` | Page |
| `ConnectorCard.jsx` | `frontend/src/components/cards/ConnectorCard.jsx` | Card |
| `OAuthFlowModal.jsx` | `frontend/src/components/modals/OAuthFlowModal.jsx` | Modal |
| `APIKeyForm.jsx` | `frontend/src/components/forms/APIKeyForm.jsx` | Form |
| `ConnectorTestButton.jsx` | `frontend/src/components/buttons/ConnectorTestButton.jsx` | Button |

### 2.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/integrations/connectors` | `list_connectors()` |
| POST | `/api/v1/integrations/connectors` | `create_connector()` |
| GET | `/api/v1/integrations/connectors/{id}` | `get_connector_details()` |
| POST | `/api/v1/integrations/connectors/{id}/test` | `test_connector()` |
| DELETE | `/api/v1/integrations/connectors/{id}` | `delete_connector()` |
| POST | `/api/v1/integrations/oauth/initiate` | `initiate_oauth()` |
| GET | `/api/v1/integrations/oauth/callback` | `oauth_callback()` |

### 2.3 End-to-End Acceptance Criteria

- [ ] **F5.2.1**: Card shows connector name, type, status, last sync
- [ ] **F5.2.2**: OAuth flow opens popup for third-party auth
- [ ] **F5.2.3**: API key form with masked input and validation
- [ ] **F5.2.4**: Test button verifies connection with success/error
- [ ] **F5.2.5**: Delete requires confirmation with connector name
- [ ] **I5.2.1**: OAuth redirect handled via popup callback
- [ ] **I5.2.2**: Credentials stored encrypted at rest
- [ ] **R5.2.1**: Connector schema: `{ id, name, type, status, last_sync, credentials_set }`
- [ ] **R5.2.2**: Test result: `{ success, latency_ms, error? }`

---

## Deliverable 3: External Data Sources Page

### 3.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `ExternalDataSources.jsx` | `frontend/src/pages/data-scientist/ExternalDataSources.jsx` | Page |
| `ProviderCard.jsx` | `frontend/src/components/cards/ProviderCard.jsx` | Card |
| `SubscriptionConfig.jsx` | `frontend/src/components/forms/SubscriptionConfig.jsx` | Form |
| `DataPreviewTable.jsx` | `frontend/src/components/tables/DataPreviewTable.jsx` | Table |
| `CostEstimator.jsx` | `frontend/src/components/widgets/CostEstimator.jsx` | Widget |

### 3.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/external/providers` | `list_data_providers()` |
| GET | `/api/v1/external/providers/{id}` | `get_provider_details()` |
| POST | `/api/v1/external/providers/{id}/subscribe` | `subscribe_to_feed()` |
| GET | `/api/v1/external/providers/{id}/preview` | `preview_data()` |
| GET | `/api/v1/external/usage` | `get_usage_stats()` |

### 3.3 End-to-End Acceptance Criteria

- [ ] **F5.3.1**: Provider cards show Alpha Vantage, Finnhub, Polygon.io, etc.
- [ ] **F5.3.2**: Subscription config selects symbols, frequency, fields
- [ ] **F5.3.3**: Data preview shows sample records from feed
- [ ] **F5.3.4**: Cost estimator calculates API call costs
- [ ] **F5.3.5**: Usage stats show daily/monthly API call counts
- [ ] **I5.3.1**: Subscribe POST creates background ingestion job
- [ ] **I5.3.2**: Preview limited to 100 records
- [ ] **R5.3.1**: Provider schema: `{ id, name, available_feeds[], pricing_tier }`
- [ ] **R5.3.2**: 402 Payment Required if rate limit exceeded

---

## Deliverable 4: Webhook Receiver Page

### 4.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `WebhookReceiver.jsx` | `frontend/src/pages/admin/WebhookReceiver.jsx` | Page |
| `WebhookEndpointCard.jsx` | `frontend/src/components/cards/WebhookEndpointCard.jsx` | Card |
| `WebhookLogTable.jsx` | `frontend/src/components/tables/WebhookLogTable.jsx` | Table |
| `CreateWebhookModal.jsx` | `frontend/src/components/modals/CreateWebhookModal.jsx` | Modal |
| `PayloadInspector.jsx` | `frontend/src/components/panels/PayloadInspector.jsx` | Panel |

### 4.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/webhooks` | `list_webhooks()` |
| POST | `/api/v1/webhooks` | `create_webhook()` |
| DELETE | `/api/v1/webhooks/{id}` | `delete_webhook()` |
| GET | `/api/v1/webhooks/{id}/logs` | `get_webhook_logs()` |
| POST | `/api/v1/webhooks/inbound/{secret}` | `receive_webhook()` |
| POST | `/api/v1/webhooks/{id}/test` | `send_test_payload()` |

### 4.3 End-to-End Acceptance Criteria

- [ ] **F5.4.1**: Endpoint card shows URL, secret key (masked), status
- [ ] **F5.4.2**: Create modal generates unique secret and URL
- [ ] **F5.4.3**: Log table shows received payloads with timestamp
- [ ] **F5.4.4**: Payload inspector shows formatted JSON/XML
- [ ] **F5.4.5**: Test button sends sample payload to configured handler
- [ ] **I5.4.1**: Inbound webhooks validated via HMAC signature
- [ ] **I5.4.2**: Logs retained for 30 days
- [ ] **R5.4.1**: Webhook schema: `{ id, url, secret, created_at, request_count }`
- [ ] **R5.4.2**: 401 Unauthorized for invalid signature

---

## Deliverable 5: Data Quality Dashboard Widget

### 5.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `DataQualityWidget.jsx` | `frontend/src/components/widgets/DataQualityWidget.jsx` | Widget |
| `QualityScoreGauge.jsx` | `frontend/src/components/charts/QualityScoreGauge.jsx` | Chart |
| `QualityIssuesTable.jsx` | `frontend/src/components/tables/QualityIssuesTable.jsx` | Table |
| `FreshnessIndicator.jsx` | `frontend/src/components/indicators/FreshnessIndicator.jsx` | Indicator |

### 5.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/ingestion/quality/summary` | `get_quality_summary()` |
| GET | `/api/v1/ingestion/quality/issues` | `list_quality_issues()` |
| GET | `/api/v1/ingestion/quality/sources/{source}` | `get_source_quality()` |
| POST | `/api/v1/ingestion/quality/issues/{id}/resolve` | `resolve_issue()` |

### 5.3 End-to-End Acceptance Criteria

- [ ] **F5.5.1**: Gauge shows overall quality score (0-100)
- [ ] **F5.5.2**: Issues table shows nulls, duplicates, schema violations
- [ ] **F5.5.3**: Freshness indicator shows time since last update per source
- [ ] **F5.5.4**: Drill-down shows quality metrics per data source
- [ ] **F5.5.5**: Resolve button marks issue as acknowledged
- [ ] **I5.5.1**: Quality checks run automatically on ingestion
- [ ] **I5.5.2**: Alerts triggered for critical quality drops
- [ ] **R5.5.1**: Summary schema: `{ score, completeness_pct, accuracy_pct, freshness_hours }`
- [ ] **R5.5.2**: Issue schema: `{ id, type, source, severity, detected_at, sample_rows[] }`

---

## Testing Requirements

| Test Suite | Description |
|------------|-------------|
| `test_phase5_pipeline_e2e.py` | DAG view → trigger → monitor run |
| `test_phase5_connector_e2e.py` | Create → OAuth → test → sync |
| `test_phase5_webhook_e2e.py` | Create → receive → inspect payload |
| `test_phase5_quality_e2e.py` | Check quality → view issues → resolve |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 5 Implementation Plan - Version 1.0*
