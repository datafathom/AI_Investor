# Context Window Manager (Agent 17.6)

## ID: `context_window_manager`

## Role & Objective
The 'System Optimizer'. Dynamically adjusts temperature, top-p, frequency penalties, and "Context Window" depth for all agents based on the urgency and nature of the task.

## Logic & Algorithm
- **Hyperparameter Tuning**: Lowers "Temperature" for financial calculations and increases it for "Creative Strategy brainstorming."
- **Focus Narrowing**: Automatically trims long conversation histories to fit within the "Sweet Spot" of a model's context window.
- **Self-Correction Trigger**: If a model produces a "Garbage" or recursive output, this agent resets the parameters and tries a different configuration.

## Inputs & Outputs
- **Inputs**:
  - `active_task_metadata` (Dict): Urgency, type, and source.
- **Outputs**:
  - `llm_parameter_set` (Dict): Temp, TopP, MaxTokens, ContextDepth.

## Acceptance Criteria
- Ensure 0% "Context Overflow" errors across the entire workforce.
- Achieve a 10% improvement in "Task Precision" through task-specific hyperparameter tuning.
