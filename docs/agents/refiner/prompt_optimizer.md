# Prompt Optimizer (Agent 17.4)

## ID: `prompt_optimizer`

## Role & Objective
The 'Signal Extractor'. Sanitizes raw data feeds and complex user requests into "Prompt-Ready" structures that maximize the reasoning capabilities of the agent workforce.

## Logic & Algorithm
- **Information Density Maximization**: Rephrases clunky user requests into structured systemic instructions.
- **Context Prioritization**: Moves the most critical data points to the "Start" or "End" of the prompt to avoid "Lost in the Middle" errors.
- **Instruction Injection**: Automatically adds mandatory safety and formatting constraints to every outgoing prompt.

## Inputs & Outputs
- **Inputs**:
  - `raw_interactive_input` (Text).
- **Outputs**:
  - `optimized_prompt_structure` (Text): The refined instruction set.

## Acceptance Criteria
- Increase "First-Shot Success Rate" for complex tasks by 15% through prompt refinement.
- Ensure 100% of optimized prompts include the "Zero-Trust" safety headers.
