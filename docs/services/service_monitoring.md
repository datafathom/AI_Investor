# Backend Service: Monitoring (System Vitals)

## Overview
The **Monitoring Service** is the platform's "Central Nervous System," providing real-time observability into the health, performance, and security of the Sovereign OS. It aggregates metrics from all other services, tracking CPU/RAM usage, API latency, and application errors. It also serves as the dispatch hub for critical alerts, routing them to the appropriate human channels (Slack, PagerDuty, SMS) based on severity.

## Core Components

### 1. Alert Manager (`alert_manager.py`)
The unified notification dispatcher.
- **Multi-Channel Routing**: Intelligent logic that routes alerts based on severity:
    - **INFO/WARNING** -> Slack Channels.
    - **ERROR** -> Email + Slack.
    - **CRITICAL** -> PagerDuty + SMS + All Channels.
- **Context Enrichment**: automatically attaches timestamps, metadata, and stack traces to every alert payload.

### 2. Error Tracker (`error_tracker.py`)
Production-grade exception monitoring.
- **Sentry Integration**: Wraps the Python application with the Sentry SDK to capture unhandled exceptions, performance transactions, and breadcrumbs.
- **PII Scrubbing**: Configured to strip sensitive financial data from error logs before they leave the secure enclave.

### 3. Health & Latency Monitors (`health_monitor.py`, `latency_monitor.py`)
Real-time system pulse tracking.
- **Resource Vitals**: Tracks CPU, Memory, and Disk usage to detect "Zombie Services" or memory leaks via `psutil`.
- **E2E Latency**: Measures the round-trip time for critical market events (Redpanda Ingest -> Postgres Commit), alerting if processing lag exceeds 200ms.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **System Monitor** | DB Health Gauges | `health_monitor.get_system_vitals()` | **Implemented** (`DatabaseGauges.jsx`) |
| **System Monitor** | Data Source Pulse | `latency_monitor.get_average_latency()` | **Implemented** (`DataSourceHealth.jsx`) |
| **Sentry Station** | Audit Log Stream | `error_tracker` (via API logs) | **Implemented** (`SentryAudit.jsx`) |
| **Sentry Station** | Security Vault Status | `health_monitor.check_service_health()`| **Implemented** (`SentryVault.jsx`) |

## Dependencies
- `psutil`: Cross-platform library for retrieving information on running processes and system utilization.
- `sentry_sdk`: The official Python client for Sentry.io.
- `twilio`: (Optional) Library for sending SMS alerts for critical failures.

## Usage Examples

### Dispatching a Critical System Alert
```python
from services.monitoring.alert_manager import get_alert_manager, AlertLevel

alerter = get_alert_manager()

# Database connection lost - Wake up the admin!
alerter.send_alert(
    message="CRITICAL: Primary Postgres Connection Failed [ECONNREFUSED]",
    level=AlertLevel.CRITICAL,
    channels=None, # Auto-selects PagerDuty + SMS
    context={"node": "worker-01", "retry_count": 5}
)
```

### Checking System Health Vitals
```python
from services.monitoring.health_monitor import get_health_monitor

physician = get_health_monitor()
vitals = physician.get_system_vitals()

if vitals["status"] == "CRITICAL_LOAD":
    print(f"WARNING: CPU at {vitals['cpu_percent']}% | RAM at {vitals['memory_percent']}%")
else:
    print(f"System Healthy. CPU: {vitals['cpu_percent']}%")
```
