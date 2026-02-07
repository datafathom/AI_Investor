# Backend Service: Infrastructure

## Overview
The **Infrastructure Service** is the foundation upon which the entire Sovereign OS is built. It provides the "Global Nervous System" (Event Bus) for inter-service communication, high-performance caching for AI operations, and the orchestration of the platform's self-hosted, ZFS-backed **Private Cloud**. It ensures low-latency response times, data redundancy, and unified state management across the distributed architecture.

## Core Components

### 1. Global Event Bus (`event_bus.py`)
The architectural backbone for reactive, event-driven logic.
- **Pub/Sub Orchestration**: Allows asynchronous communication between services. For example, the discovery of a "Liquidity Crisis" in the risk service can be broadcast to the trading terminal and notifications engine simultaneously.
- **Topic-Based Routing**: Facilitates specialized subscription channels for high-priority signals (e.g., Geopolitical Shocks, System Heartbeats).

### 2. Agent Response Cache (`cache_service.py`)
Optimizes AI latency and operational costs.
- **MD5-Based Persistence**: Generates unique cryptographic keys for every agent-prompt pair, storing the resulting LLM responses in a persistent JSON cache.
- **Latency Reduction**: Automatically hits the cache for repeated queries, ensuring that "Agentic Thinking" is instantaneous for known scenarios.

### 3. Private Cloud Manager (`private_cloud.py`)
Manages the platform's physical data sovereignty.
- **ZFS Integration**: Interfaces with self-hosted storage tanks (RAID-Z2) to provide high-redundancy document storage.
- **Quota Monitoring**: Dynamically tracks available TBs and storage health, ensuring that the platform's large-scale data logs and document archives have sufficient headroom.
- **Sovereign Sync**: Handles the encrypted upload of sensitive financial documents to a private Nextcloud instance.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **System Monitor** | Event Bus Feed | `event_bus_service.publish()` (Signal log) |
| **Settings Panel** | Storage Quota Ring | `private_cloud_service.check_storage_quota()` |
| **Admin Panel** | Cache Hit/Miss Pulse | `agent_response_cache.get()` |
| **Document Vault** | Sovereign Cloud Sync Status| `private_cloud_service.sync_document()` |
| **Mission Control** | System Health Sparklines | `telemetry_service` (Heartbeats) |

## Dependencies
- `hashlib`: Generates unique keys for the agent response cache.
- `ZFS / Nextcloud`: (Infrastructure) The underlying storage and cloud technology stacks.
- `json`: Standard persistence format for local state and lightweight caching.

## Usage Examples

### Publishing a Geopolitical Shock Signal
```python
from services.infrastructure.event_bus import EventBusService

bus = EventBusService()

# Broadcast a major market event
bus.publish(
    topic="GEOPOLITICAL_SHOCK",
    payload={
        "region": "MIDDLE_EAST",
        "severity": "CRITICAL",
        "timestamp": "2026-02-06T12:00:00Z"
    }
)
```

### Retrieving an AI Completion from Cache
```python
from services.infrastructure.cache_service import get_agent_cache

cache = get_agent_cache()

# Attempt to fetch a previous completion
cached_response = cache.get(
    agent_id="STRATEGIST_AG_01",
    prompt="Summarize the impact of 5% interest rates on growth equity."
)

if cached_response:
    print(f"CACHE HIT: {cached_response[:100]}...")
```

### Checking Cloud Storage Health
```python
from services.infrastructure.private_cloud import PrivateCloudService

cloud = PrivateCloudService()

stats = cloud.check_storage_quota()
print(f"Cloud Status: {stats['status']} | Free Space: {stats['free_tb']} TB")
print(f"Redundancy: {stats['redundancy']}")
```
