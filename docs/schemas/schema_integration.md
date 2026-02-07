# Schema: Integration

## File Location
`schemas/integration.py`

## Purpose
Pydantic models for third-party integrations and data synchronization. Manages connections to external apps like Mint, YNAB, and Personal Capital for aggregated financial data.

---

## Enums

### IntegrationStatus
**Status of third-party integration.**

| Value | Description |
|-------|-------------|
| `CONNECTED` | Active connection |
| `DISCONNECTED` | Not connected |
| `ERROR` | Connection error |
| `SYNCING` | Data sync in progress |

---

## Models

### Integration
**Third-party integration configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `integration_id` | `str` | *required* | Unique integration ID | Primary key |
| `user_id` | `str` | *required* | Integration owner | Attribution |
| `app_name` | `str` | *required* | App name: `mint`, `ynab`, `personal_capital` | App identification |
| `status` | `IntegrationStatus` | `DISCONNECTED` | Connection status | State tracking |
| `oauth_token` | `Optional[str]` | `None` | OAuth access token | Authentication |
| `last_sync_date` | `Optional[datetime]` | `None` | Last successful sync | Freshness |
| `sync_frequency` | `str` | `"daily"` | Sync schedule: `realtime`, `hourly`, `daily`, `manual` | Scheduling |
| `created_date` | `datetime` | *required* | Connection timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Tracking |

---

### SyncJob
**Data synchronization job.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `sync_job_id` | `str` | *required* | Unique job ID | Primary key |
| `integration_id` | `str` | *required* | Parent integration | Linking |
| `sync_type` | `str` | *required* | Type: `full`, `incremental` | Sync strategy |
| `status` | `str` | `"pending"` | Status: `pending`, `running`, `completed`, `failed` | Workflow |
| `started_date` | `Optional[datetime]` | `None` | Job start time | Timing |
| `completed_date` | `Optional[datetime]` | `None` | Job end time | Timing |
| `records_synced` | `int` | `0` | Records synchronized | Progress |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `IntegrationFramework` | Integration infrastructure |
| `IntegrationService` | Connection management |
| `SyncService` | Data synchronization |
| `OAuthService` | Token management |

## Frontend Components
- Integration dashboard (FrontendIntegration)
- Connection wizard
- Sync status display
