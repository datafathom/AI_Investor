# Department Agent (`department_agent.py`)

## Description
The `DepartmentAgent` is a specialized subclass of `BaseAgent` designed to function within a specific department (e.g., "Strategist", "Trader", "Auditor"). It handles domain-specific event routing and uses tailored prompt templates.

## Role in Department
This is the workhorse class for categorized agents. It provides the boilerplate for department-specific behavior, such as updating telemetry and loading specialized prompts from the `agents/prompts/` directory.

## Input & Output
- **Input**: Department-specific events (e.g., `audit.reconcile`) and task payloads.
- **Output**: Telemetry updates and success/error responses from LLM invocations.

## Key Features
- **Prompt Isolation**: Loads system and user prompts specific to the agent's role (e.g., `department_agent_system.txt`).
- **Telemetry**: Automatically publishes status and performance metrics to the department's event topic (e.g., `dept.1.agents`).
- **Agnostic Invocation**: Can be directly invoked for specialized tasks with a standard payload.

## Pipelines & Integration
- **Event Bus**: Extensively uses `EventBusService` to broadcast its status across its department.
- **Prompt Loader**: Connects to the centralized prompt repository for consistency across 84+ agents.
