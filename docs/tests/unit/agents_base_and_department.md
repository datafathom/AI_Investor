# Documentation: `tests/unit/test_base_agent.py` & `test_department_agent.py`

## Overview
These tests cover the fundamental building blocks of the AI workforce. They ensure that all agents inherit the necessary lifecycle states and can communicate via the central event bus.

## Services Under Test
- `agents.base_agent.BaseAgent`: Abstract base class for all agents.
- `agents.department_agent.DepartmentAgent`: Standard implementation for functional departments.

## Test Scenarios

### 1. Agent Lifecycle (`test_base_agent.py`)
- **Goal**: Verify that any agent can be started, stopped, and queried for health.
- **Assertions**:
    - Initialization defaults to `inactive`.
    - `start()` sets `is_active=True`.
    - `health_check()` returns structured telemetry including name and status.

### 2. Departmental Invocation (`test_department_agent.py`)
- **Goal**: Verify that a department agent can execute a task using an LLM.
- **Assertions**:
    - `invoke()` successfully calls the LLM (mocked) and returns a structured response.
    - Integration with `EventBusService` is verified by checking that responses are published to the correct department-specific topic (e.g., `dept.1.agents`).
    - Error handling gracefully catches and logs LLM failures.

## Holistic Context
These tests define the "Agent Protocol". By ensuring every agent follows these rules, the system maintains a consistent orchestration layer regardless of the specific task (trading, research, etc.) the agent performs.
