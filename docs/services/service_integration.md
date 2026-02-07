# Backend Service: Integration

## Overview
The **Integration Service** serves as the platform's universal connector hub. It provides a standardized **Framework** for linking the Sovereign OS with external financial ecosystems (e.g., Mint, YNAB, Quicken) and enterprise toolsets. By utilizing OAuth-based authentication and structured sync scheduling, it ensures that external data is seamlessly mapped and transformed into the platform's internal schemas.

## Core Components

### 1. Integration Framework (`integration_framework.py`)
The foundational infrastructure for external connectivity.
- **Provider Registry**: Maintains a list of supported third-party applications and their respective connectivity protocols.
- **OAuth Orchestration**: Handles the secure lifecycle of external connections, managing authentication tokens and connection states (`CONNECTED`, `DISCONNECTED`, `PENDING`).
- **Data Mapping Foundation**: Provides the base logic for transforming external JSON payloads into platform-compliant models.

### 2. Synchronization Engine (`integration_service.py`)
Orchestrates the movement of data between external apps and the platform.
- **Sync Job Management**: Handles the scheduling and execution of `full` and `incremental` data refreshes. It tracks the status of each job, including start/end times and the count of records successfully synchronized.
- **Conflict Resolution**: (Framework level) Provides the logic for resolving data discrepancies between external feeds and the platform's local state.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Integrations Hub** | App Store / Connector Grid | `integration_framework.get_supported_apps()` |
| **Integrations Hub** | Connection Wizard | `integration_framework.create_integration()` |
| **Sync Monitor** | Real-time Sync Pulse | `integration_service.sync_data()` |
| **Sync Monitor** | Historical Job Ledger | `integration_service.get_sync_status()` |
| **Settings Panel** | Linked Accounts Card | `integration_framework` (Connection status) |

## Dependencies
- `services.system.cache_service`: Persists integration states and synchronization logs.
- `schemas.integration`: Defines the standard `Integration` and `SyncJob` Pydantic models.
- `OAuthService`: (External) Handles the actual token exchange and refreshing.

## Usage Examples

### Linking a New External App (Mint)
```python
from services.integration.integration_framework import get_integration_framework

framework = get_integration_framework()

# User initiates a connection to Mint with a successful OAuth token
integration = await framework.create_integration(
    user_id="user_vanderbilt_001",
    app_name="mint",
    oauth_token="0x_MOCK_OAUTH_TOKEN_ABC"
)

print(f"Integration Created: {integration.integration_id}")
print(f"Current Status: {integration.status}")
```

### Triggering an Incremental Data Sync
```python
from services.integration.integration_service import get_integration_service

sync_service = get_integration_service()

# Run an incremental update for an existing YNAB connection
job = await sync_service.sync_data(
    integration_id="integration_user_001_ynab",
    sync_type="incremental"
)

print(f"Sync Job {job.sync_job_id}: {job.status}")
print(f"Records Processed: {job.records_synced}")
```
