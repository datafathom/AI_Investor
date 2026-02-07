# System Services (`services/system/`)

The "System" namespace contains the mission-critical services that provide the backbone for the Sovereign OS runtime. These services are initialized once (Singletons) and shared across the API, Workers, and Agents.

## 1. Health & Resilience
- **`health_check_service.py`**: Monitors the heartbeat of every component (DB, Redis, Kafka, Agents). Provides the unified `/health` status used by the dashboard.
- **`circuit_breaker.py`**: A utility decorator that prevents cascading failures by "tripping" when a service (like a vendor API) becomes unresponsive.

## 2. Observability & Logging
- **`logging_service.py`**: Manages the unified logging format and ensures that sensitive data (API keys, PII) is scrubbed via `scrubber.py`.
- **`tracing_service.py`**: Implements distributed tracing for multi-step agent workflows. Every "Mission" can be traced from its inception in the Orchestrator to its execution in the Worker.
- **`activity_service.py`**: Captures business-level actions (e.g., "User started a backtest") for audit logs and user activity feeds.

## 3. Security & Secrets
- **`security_gateway.py`**: Handles rate limiting and WAF rules at the application layer.
- **`secret_manager.py` / `vault_secret_manager.py`**: Abstract interfaces for retrieving sensitive configuration. Supports local `.env`, AWS Secrets Manager, and HashiCorp Vault.
- **`totp_service.py`**: Manages Time-based One-Time Password generation and validation for secure agent authorization.

## 4. Communication & Connectivity
- **`socket_manager.py`**: The bridge between the backend logic and the frontend's real-time WebSockets.
- **`kafka_monitor_service.py`**: Observes Kafka cluster health and lag, feeding performance metrics to the `TrafficControllerAgent`.

## 5. Intelligence & Models
- **`model_manager.py`**: Orchestrates connections to LLM providers (Anthropic, OpenAI, Perplexity). Handles prompt versioning and token tracking.

## Initialization Pattern
All system services follow a **Singleton** pattern (often using `__new__` or a shared `_instance` variable). This ensures that heavy resources (like engine connections or model clients) are not duplicated, maintaining a low memory footprint.
