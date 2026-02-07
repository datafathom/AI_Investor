# API Gateway (`fastapi_gateway.py`)

The API Gateway is the central hub for all real-time interactions with the Sovereign OS. It leverages **FastAPI** to provide a high-performance, asynchronous interface for the React frontend and mobile clients.

## High-Performance Core
- **Framework**: FastAPI (pydantic-based validation).
- **Server**: Uvicorn (worker processes on port 5050).
- **Concurrency**: Fully asynchronous (`async/await`) leveraging the Python `asyncio` loop.

## Routing Architecture
The gateway uses a highly modular "Router" pattern. Instead of a single monolithic file, APIs are categorized into domain-specific modules located in `web/api/`.

### Key API Categories:
- **Core Operations**: `health`, `auth`, `system`, `identity`.
- **Trading & Risk**: `brokerage`, `strategy`, `risk`, `advanced_orders`.
- **Intelligence**: `debate`, `news`, `research`, `market_data`.
- **Departmental**: `departments`, `master_orchestrator`.
- **Administrative**: `billing`, `docs`, `telemetry`.

## Middleware & Security
- **CORS Management**: Strictly configured to allow requests only from trusted sources (`localhost:5173` and `127.0.0.1:5173`).
- **Security Gateway**: Integrates `SecurityGatewayService` for rate limiting (via `InMemoryRateLimiter`) and basic WAF protections.
- **Authentication**: JWT-based authentication flow (managed via `auth_api`).

## Integrated Services & Lifecycle
The Gateway manages the lifecycle of several critical background services:
1.  **Slack Integration**: During the `startup` event, the gateway initializes the `SlackService`, announces its online status, and starts the background bot listener.
2.  **Socket.IO**: Real-time push notifications and HUD updates are handled via the mounted `socket_app` (Socket.IO Socket Mode).
3.  **Graceful Shutdown**: During `shutdown`, the gateway ensures all service connections (Redis, Slack, Postgres) are cleanly closed to prevent data corruption.

## Local Binding
As part of the system's security posture, the gateway explicitly binds to **`127.0.0.1:5050`**.
