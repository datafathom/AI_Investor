# Backend Service: Logging (Internal Telemetry)

## Overview
The **Logging Service** (specifically the **Warden Health Log**) serves as the platform's diagnostic persistence layer. It is responsible for capturing and storing the results of automated system health checks performed by the **Warden Service**. By providing a structured ledger of infrastructure stability and component availability, it enables real-time monitoring and historical analysis of the Sovereign OS's operational uptime.

## Core Components

### 1. Warden Health Log (`health_log.py`)
The system's diagnostic recorder.
- **Check-Result Persistence**: Processes and logs the detailed output of the Warden's health checks (e.g., Database connectivity, API latency, Memory usage).
- **Status Ledgering**: Standardizes check results into an `OVERALL_STATUS` (e.g., HEALTHY, DEGRADED, CRITICAL) for simplified frontend visualization and alerting.
- **Audit Traceability**: Provides a historical trace for infrastructure troubleshooting, allowing engineers to correlate system errors with specific health-check failures.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **System Monitor** | Warden Infrastructure Pulse | `health_log.log_check()` |
| **Admin Station** | Diagnostic Success Ledger | `health_log.log_check()` (Status tags) |
| **Warden Command** | Stability Trend-Line | `health_log` (Historical results) |
| **Global UI** | System Status Badge | `health_log` (Current status state) |

## Dependencies
- `datetime`: Provides micro-second precision timestamps for diagnostic event correlation.
- `logging`: Mirrors health-check results to the application-level logs for centralized log management (e.g., ELK Stack / Datadog).

## Usage Examples

### Logging a Successful System Health Check
```python
from services.logging.health_log import HealthLog

logger_svc = HealthLog()

# Mock result from the Warden service
result = {
    "timestamp": "2026-02-06T23:55:00Z",
    "overall_status": "HEALTHY",
    "services": {
        "postgres": "UP",
        "redis": "UP",
        "neo4j": "UP"
    }
}

logger_svc.log_check(check_result=result)
# Console: WARDEN_CHECK_LOG: HEALTHY - {'timestamp': ...}
```

### Logging a Degraded System State
```python
from services.logging.health_log import HealthLog

logger_svc = HealthLog()

# Mock result indicating memory pressure
result = {
    "timestamp": "2026-02-06T23:58:00Z",
    "overall_status": "DEGRADED",
    "alerts": ["JVM Memory Pressure on Searcher Agent 04"]
}

logger_svc.log_check(check_result=result)
```
