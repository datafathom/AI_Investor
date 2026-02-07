# Documentation: `tests/unit/test_websocket.py`

## Overview
This test suite validates the real-time notification engine. It ensures that agent updates, portfolio movements, and trading signals are correctly formatted before being broadcast to the frontend.

## Component Under Test
- `web.websocket.WebSocketBroadcaster`

## Key Test Scenarios

### 1. UI Telemetry Broadcasting
- **Goal**: Ensure the frontend receives actionable updates.
- **Assertions**:
    - `broadcast_agent_status` sends correct "healthy/active" flags to the `agents` room.
    - `broadcast_portfolio_update` correctly calculates and sends the "Gap" and "Gap Percent" relative to the account set-point.

### 2. Critical Signal Dispatch
- **Goal**: Verify that trading signals and risk alerts are published immediately.
- **Assertions**:
    - `broadcast_alert` correctly formats severity (low, warning, critical) and payloads.
    - `broadcast_signal` includes confidence scores and the source agent ID for auditability.

### 3. Data Integrity
- **Goal**: Standardize the "Z" (Zulu) timestamp format for global synchronization.
- **Assertions**: `_get_timestamp()` returns a valid ISO-8601 string with the trailing `Z` suffix.

## Holistic Context
The WebSocket service is the "Voice" of the AI. These tests ensure that the user (human or monitoring script) sees a high-fidelity representation of the system's internal state without lag or formatting errors.
