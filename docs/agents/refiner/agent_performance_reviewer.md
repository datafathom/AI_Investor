# Agent Performance Reviewer (Agent 17.3)

## ID: `agent_performance_reviewer`

## Role & Objective
The 'Quality Judge'. Ranks multiple LLM outputs (e.g., comparing Claude 3.5 vs. Gemini 1.5 Pro) to select the most logically sound and safe response for a given task.

## Logic & Algorithm
- **Multi-Model Consensus**: Runs critical prompts through multiple models simultaneously.
- **Voting Mechanism**: Uses a weighted "Reviewer" logic to select the best output based on adherence to instructions.
- **Dynamic Routing**: Recommends which model is "Winning" for specific categories (e.g., "Physicist tasks are better handled by Gemini").

## Inputs & Outputs
- **Inputs**:
  - `multi_model_outputs` (Dict): Responses from different AI engines.
- **Outputs**:
  - `selected_best_response` (str).
  - `leaderboard_update` (Dict): Updated performance stats for each model provider.

## Acceptance Criteria
- Achieve a "Selection Accuracy" of > 95% when compared against human expert preference.
- Maintain a latency overhead of < 500ms for the review process.
