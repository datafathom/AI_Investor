# Behavioral Analyst (Agent 12.2)

## ID: `behavioral_analyst`

## Role & Objective
The 'Self-Reflection' engine. Grades the system's performance on rule adherence versus impulsive deviations, ensuring the "Sovereign OS" remains disciplined.

## Logic & Algorithm
- **Variance Audit**: Compares executed trades against the Strategist's "Golden Rules" (e.g., max position size).
- **Rule Grader**: Assigns an "Impulse Score" to any trade that breaks pre-defined logic but was forced through.
- **Sentiment Correlation**: Cross-references the user's "Readiness Score" (from Wellness Sync) with system-driven rule violations.

## Inputs & Outputs
- **Inputs**:
  - `system_configuration` (Rules): The defined trading constraints.
  - `execution_stream` (Data): Chronological list of trade events.
- **Outputs**:
  - `discipline_grade` (A-F): Overall rating of system adherence to policy.

## Acceptance Criteria
- Identify 100% of "Rule Breaking" events within 1 hour of execution.
- Maintain a cumulative "System Integrity" score of > 95%.
