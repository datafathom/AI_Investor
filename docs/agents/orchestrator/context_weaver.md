# Context Weaver (Agent 1.6)

## ID: `context_weaver`

## Role & Objective
The system's short-term memory manager. It ensures that when a user or agent switches contexts (e.g., from Portfolio view to Tax view), the relevant history is injected so no information is lost.

## Logic & Algorithm
1. **Session Buffering**: Maintains a sliding window of the last 5 critical actions.
2. **Redis Coordination**: Persists context across Docker container restarts for zero-loss state.
3. **Knowledge Injection**: Dynamically builds prompt prefixes for LLM-based agents based on recent activity.

## Inputs & Outputs
- **Inputs**:
  - Agent Action Completion Events
  - Role-Switch Signals
- **Outputs**:
  - Formatted Context Strings
  - Redis State Updates

## Acceptance Criteria
- Injects 100% of the last 5 relevant actions into departmental role-switches.
- Context lookup latency must be < 10ms.
