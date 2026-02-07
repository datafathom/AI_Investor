# Background Workers (`worker.py`)

The Sovereign OS uses an asynchronous background execution engine based on **ARQ** (Redis-based job queue). This ensures that long-running operations—such as strategy backtests, market scraping, or complex agent reasoning—do not block the main API gateway.

## Core Component: `worker.py`

The worker is a dedicated process that consumes tasks from Redis and executes them in a managed context.

### Key Logic: `run_agent_logic`
- **Execution**: The primary entry point for agent logic within the worker.
- **Mission Context**: Receives a `mission_data` payload containing the department, mission ID, and task specifics.
- **Experience Storage**: Every executed mission is analyzed and stored in the `memory_service` as a new "Experience" node, contributing to the system's long-term learning.

## Lifecycle Management
The worker manages its own internal state via lifecycle hooks:
1.  **`startup`**: Initializes the `DatabaseManager` and attaches it to the worker context (`ctx`). Ensures that all task executions have immediate, high-availability access to Postgres.
2.  **`shutdown`**: Cleanly releases database pools and signals the job queue to stop accepting new tasks.

## Configuration (`WorkerSettings`)
- **Queue Engine**: Uses Redis (defaulting to `127.0.0.1:6379`).
- **Function Registry**: Functions like `run_agent_logic` are explicitly registered to be callable via the `mission_id` protocol.
- **Serialization**: Uses binary serialization for high-performance data transfer between the API and the Worker.

## Scalability & Monitoring
- **Parallelism**: Multiple worker processes can be started to scale horizontally.
- **Observability**: Worker health and queue depth are monitored by the `HealthCheckService`.
- **Fault Tolerance**: Failed jobs are automatically retried based on configurable policies in the `WorkerSettings`.
