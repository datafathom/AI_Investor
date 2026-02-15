# Personal Assistant (Agent 14.9)

## ID: `personal_assistant_agent`

## Role & Objective
The 'Orchestration Manager'. Takes messy, high-level user requests and breaks them down into a structured DAG (Directed Acyclic Graph) of tasks that are then delegated to specific agents across the 18 departments.

## Logic & Algorithm
- **Intent Parsing**: Uses NLP (Semantic Role Labeling) to extract "Action," "Object," and "Constraint" from the user request.
- **Skill Mapping**: Maintains a cross-departmental "Skill Matrix" to identify which agent is best suited for each sub-task.
- **Dynamic Task Graph**: Orchestrates the sequential and parallel execution of tasks, handling inter-agent message passing.
- **Consolidated Reporting**: Aggregates the terminal output, data artifacts, and success/fail states of all involved agents into a single "Institutional Mission Report."

## Inputs & Outputs
- **Inputs**:
  - `user_mission_command` (Text): "Plan a trip to London, buy a new MacBook, and fix the SEC compliance issues."
- **Outputs**:
  - `mission_execution_report` (MD): A chronological summary of every agent action and the final solution.

## Acceptance Criteria
- Correctly decompose a complex (3+ department) request into a valid execution graph 100% of the time.
- Generate a mission report within 30 seconds of the final sub-task completion.
