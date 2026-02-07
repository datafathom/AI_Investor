# Documentation: `tests/unit/test_agent_federation.py` & `test_agent_orchestration_service.py`

## Overview
These tests validate the "Federated Workforce" model, where agents can delegate sub-tasks to each other, and the orchestration service that manages the lifecycle of all agents.

## Services Under Test
- `services.agent_orchestration_service.AgentOrchestrationService`: Central registry and factory.
- `Agent Federation (Delegation Flow)`: The `request_help()` sequence.

## Test Scenarios

### 1. Orchestration Lifecycle
- **Goal**: Ensure agents are lazy-loaded and cached correctly.
- **Assertions**:
    - Singleton pattern is enforced.
    - `get_agent()` correctly creates a new instance on first call and retrieves it from cache on subsequent calls.

### 2. Delegation Logic (Federation)
- **Goal**: Verify that an agent can request help from another.
- **Assertions**:
    - `request_help()` properly formats and sends a task request to the `AgentOrchestrationService`.
    - The delegation API endpoint (`/delegate`) correctly extracts source/target IDs and verifies existence before proceeding.

## Holistic Context
Federation is what allows the system to scale from simple scripts to a complex 84-agent workforce. These tests ensure the "chain of command" is reliable and that the central service can manage high volumes of inter-agent communication.
