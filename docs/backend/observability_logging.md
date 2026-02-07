# Observability & Logging

A system with 84+ agents requires high-fidelity observability to ensure stability and transparency. The Sovereign OS implements a multi-layer observability stack covering structured logging, business tracing, and real-time telemetry.

## 1. Structured Logging (`utils/logging.py`)

The system uses a unified Python logging configuration to ensure consistency across the API, Workers, and Agents.

- **Universal Format**: `[TIMESTAMP] [LEVEL] [LOGGER_NAME]: MESSAGE`
- **Levels**: Automatically configured via the `.env` `LOG_LEVEL` (defaulting to `INFO`).
- **Destinations**: Logs are emitted to `stdout` for container orchestration (Docker) and optionally persisted to `logs/app.log`.
- **Security**: The `Scrubber` utility automatically intercepts log records to remove sensitive data (PII, API Keys, Tokens) before they hit the terminal or disk.

## 2. Business Tracing (`TracingService`)

While standard logs track "What" happened, the `TracingService` tracks "How" and "Why."

- **Mission Mapping**: Every request is assigned a unique `mission_id`. This ID is passed between the Gateway, Kafka, and Workers, allowing for a complete trace of a single decision path.
- **Agent Telemetry**: Agents emit specialized telemetry events to Kafka. These events describe their internal state transitions (e.g., `THINKING` -> `ACTING` -> `SUCCESS`).

## 3. Real-Time HUD Updates

Real-time observability is pushed to the frontend via the `SocketManager`:
- **Live Logs**: Critical system logs are streamed to the OS "Terminal" widget.
- **Health Feed**: Components publish their status pulses, which the React frontend visualizes as a "System Health" quadrant.
- **HUD Morphing**: High-priority alerts (Level: `CRITICAL`) trigger immediate HUD layout changes via the `LayoutMorphologistAgent`.

## 4. Audit Integrity (`AuditIntegrityService`)

For financial transparency, all trades and state-modifying actions are captured in the `ActivityStore`.
- **Immutable Ledger**: Logged actions are timestamped and assigned a cryptographic hash to ensure they cannot be posthumously altered.
- **Human Review**: Critical alerts requiring human input (e.g., a "Reject" from the `ProtectorAgent`) are mirrored to the Slack `#alerts` channel with full context.
