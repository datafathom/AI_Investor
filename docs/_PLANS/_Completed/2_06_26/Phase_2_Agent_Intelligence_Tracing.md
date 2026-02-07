# Phase 2: Agent Intelligence & Tracing

## Overview
This phase upgrades the agent's core decision-making architecture from "Prompt-and-Pray" to deterministic Finite State Machines (FSM). It also implements a full-spectrum "Observability Trace" that allows us to view the agent's inner monologue, tool calls, and state transitions in real-time without cluttering the main business logs.

## Deliverables

### 1. Deterministic State Machine (FSM) Support
**Description**: Integrate a state-management layer into `BaseAgent` to enforce valid operational transitions.
- **Acceptance Criteria**:
  - Agents can only enter the `EXECUTING` state after passing through `ANALYZING` and `VERIFYING`.
  - Any invalid state transition triggers an immediate `SECURITY_HALT`.
  - Agent state is persisted in Redis to allow for recovery after a container restart.

### 2. "Inner Monologue" Tracing Middleware
**Description**: A non-blocking telemetry layer that captures agent "thoughts" (LLM reasoning) before they are stripped for output.
- **Acceptance Criteria**:
  - `emit_trace` function successfully sends structured JSON to the `TRACE_` Socket.io namespace.
  - Trace logs are stored in a dedicated partitioned table in Postgres for historical review.
  - Traces include a `step_id` and `parent_job_id` for recursive reasoning tracking.

### 3. Real-Time Logic Terminal (React)
**Description**: A high-performance vertical timeline component that streams trace events to the dashboard.
- **Acceptance Criteria**:
  - Log entries are rendered with distinct styling for `THOUGHT`, `TOOL_CALL`, `REDACTION`, and `ERROR`.
  - Component uses `react-virtuoso` to handle >1,000 log lines without UI lag.
  - An "Auto-scroll" feature maintains focus on the latest agent activity during active missions.

### 4. Queue Management HUD
**Description**: An interface to monitor the current state of the ARQ worker queue.
- **Acceptance Criteria**:
  - Displays a list of `QUEUED`, `IN_PROGRESS`, and `FAILED` jobs with their associated Mission IDs.
  - A "Kill" button successfully sends an `ABORT` signal to the specific worker process.
  - Latency metrics (Time in Queue) are displayed for each job.

### 5. Pydantic-Based Tool Validation
**Description**: Enforcement of strict JSON schemas for all tool calls made by agents.
- **Acceptance Criteria**:
  - Tool signatures are automatically generated from Pydantic models.
  - malformed tool calls from LLMs are intercepted and returned with a granular error message for self-correction.
  - 100% of "Financial" tools (swap, transfer) require schema validation before execution.

### 6. Logic Persistence & Snapshotting
**Description**: Mechanisms to save and restore the "Mental State" of an agent during long-running tasks.
- **Acceptance Criteria**:
  - Agent can be "Paused" and its entire memory stack serialized to Redis.
  - "Resuming" a task restores the exact state-machine position and local memory context.
  - State snapshots are encrypted with the `DEPT_SECRET` before storage.

## Proposed Changes

### [Backend] [Agents]
- [MODIFY] [base_agent.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/agents/base_agent.py): Integration of FSM logic.
- [NEW] [state_manager.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/state_manager.py): Redis key-space management for agent states.

### [Frontend] [Components]
- [NEW] [AgentMonologue.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/AgentMonologue.jsx): The Trace UI.
- [NEW] [TaskDashboard.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/TaskDashboard.jsx): The Queue HUD.

## Verification Plan

### Automated Tests
- `pytest tests/agents/test_fsm_integrity.py`
- `pytest tests/services/test_trace_streaming.py`

### Manual Verification
- Observe "Inner Monologue" timeline during a mock "Scan Project" mission.
- Force-kill a job from the HUD and verify worker termination in console.
