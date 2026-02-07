# Documentation: `tests/api/test_health_api.py`

## Overview
This test suite validates the system's observability endpoints. It ensures that the health, readiness, and liveness probes accurately reflect the status of the service and its critical dependencies (Postgres, Redis).

## API Endpoints Under Test
- `GET /health`: Basic health check.
- `GET /health/readiness`: Kubernetes-style readiness probe (checks DB/Cache).
- `GET /health/liveness`: Basic process liveness probe.
- `GET /health/detailed`: Comprehensive system telemetry (CPU, Memory, Latency).

## Fixtures
- `mock_health_service`: Mocks the `HealthCheckService` to simulate dependency statuses and latencies.
- `mock_system_health_service`: Mocks the `SystemHealthService` for hardware telemetry.

## Test Scenarios

### 1. `test_health_check_success`
- **Goal**: Verify basic application responsiveness.
- **Assertions**: Returns 200 OK with `status: healthy`.

### 2. `test_readiness_check_success/failure`
- **Goal**: Verify that readiness accurately reflects dependency health.
- **Assertions**:
    - Returns 200 OK when Postgres/Redis are `UP`.
    - Returns 503 Service Unavailable when a critical dependency is `DOWN`.

### 3. `test_detailed_health_success`
- **Goal**: Verify that granular system data is exposed.
- **Assertions**: Returns system telemetry including CPU and memory usage.

## Holistic Context
Health APIs are used by orchestrators (Docker/K8s) to manage the service lifecycle. Correctness here prevents "traffic black holes" where requests are routed to a service that cannot reach its database.
