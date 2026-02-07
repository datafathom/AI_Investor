# Base Agent (`base_agent.py`)

## Description
The `BaseAgent` is the abstract base class (ABC) for all agents within the Sovereign OS. It defines the mandatory interface and provides core functionalities such as state management, observability (tracing), LLM integration, and tool execution.

## Role in Department
As an abstract base, it doesn't belong to a specific department but serves as the DNA for every agent in the system. It ensures that all agents follow the same lifecycle (start/stop/health) and communication protocols.

## Input & Output
- **Input**: `Dict[str, Any]` (Typically a Kafka event payload or a direct invocation request).
- **Output**: `Optional[Dict[str, Any]]` (Response or action to be taken).

## Pipelines & Integration
- **State Management**: Integrates with `StateManagerService` (Redis-backed FSM) to persist and restore agent states.
- **Observability**: Uses `SocketManager` for live HUD updates and `DatabaseManager` for persistent audit logs of every action.
- **LLM Routing**: Connects to `ModelManager` to provide LLM-agnostic completion capabilities.
- **Tool Execution**: Integrates with `ToolRegistry` to execute specialized tools with Pydantic validation and sector isolation checks.

## Key Methods
- `transition_to(new_state, reason)`: Managed state transitions with FSM validation.
- `emit_trace(label, content, type, metadata)`: Real-time observability and logging.
- `get_completion(prompt, system_message)`: LLM completion interface with caching.
- `execute_tool(tool_name, tool_args)`: Secure tool execution with sector isolation.
- `process_event(event)`: Abstract method to be implemented by child agents.
