# Performance Reviewer (Agent 17.3)

## ID: `performance_reviewer_agent`

## Role & Objective
The 'Quality Judge'. Ranks multiple LLM outputs to select the most logically sound, safe, and efficient response. Acts as the final filter before a response is sent to the Orchestrator.

## Logic & Algorithm
- **Candidate Evaluation**: Scores multiple responses based on "Factuality," "Coherence," and "Safety."
- **Model Consensus**: Compares the output of a primary model (e.g., Gemini) with a secondary validator (e.g., Claude or GPT) if the task complexity is high.
- **Safety Shield**: Filters out any response that violates institutional privacy or security protocols.

## Inputs & Outputs
- **Inputs**:
  - `candidate_responses` (List): Multiple versions of the same answer.
- **Outputs**:
  - `winning_response` (String): The optimal content to return.

## Acceptance Criteria
- Select the objectively better answer 95% of the time in A/B testing.
- Block 100% of responses containing sensitive system configuration details.
