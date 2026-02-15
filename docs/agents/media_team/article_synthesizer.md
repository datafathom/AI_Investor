# Article Synthesizer (Agent 19.1)

## ID: `article_synthesizer`

## Role & Objective
The 'Ghostwriter'. Generates high-quality blog posts, articles, and long-form content based on institutional data, market research, and system events.

## Logic & Algorithm
- **Data Distillation**: Extracts key performance metrics and market signals to serve as the "ground truth" for content.
- **Narrative Framing**: Adapts the tone (e.g., Professional, Visionary, Urgent) based on the target audience and platform.
- **Fact-Checking Loop**: Queries the Data Scientist to verify any numerical claims made within the draft.

## Inputs & Outputs
- **Inputs**:
  - `content_prompt` (Text): "Write a quarterly review of our portfolio performance."
  - `system_data_feed` (JSON).
- **Outputs**:
  - `draft_article` (MD): Markdown-formatted content with charts and citations.

## Acceptance Criteria
- Produce a 500-word draft in < 45 seconds.
- Maintain 100% accuracy for all cited percentages and price points.
