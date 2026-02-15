# Pattern Recognition Bot (Agent 15.4)

## ID: `pattern_recognition_bot`

## Role & Objective
The 'Storyteller'. Converts raw logs and high-dimensional data into long-form retrospectives, "Quarterly Reports," and tactical debriefs for the user.

## Logic & Algorithm
- **Narrative Synthesis**: Aggregates the Auditor's "Mistake Classifier" output into a monthly "Lessons Learned" story.
- **Anomaly Highlighting**: Points out "First Time Ever" events (e.g., "The highest drawdown in system history").
- **Visualization Mapping**: Generates the "Story Mode" data for the GUI, linking text descriptions to specific data points.

## Inputs & Outputs
- **Inputs**:
  - `behavioral_audit_logs` (Data): Grades and mistake tags.
  - `pnl_report_cards` (Data): Performance metrics.
- **Outputs**:
  - `quarterly_reflective_report` (MD): A human-readable narrative of the system's "Life".

## Acceptance Criteria
- Produce a monthly "Retrospective" that correctly identifies the top 3 drivers of profit and loss.
- Generate narrative text that is 100% factually grounded in the system's internal data.
