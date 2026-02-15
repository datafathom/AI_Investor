# Recovery Path Planner (Agent 16.5)

## ID: `recovery_path_planner`

## Role & Objective
The 'Resilience Scorer'. Evaluates the outcomes of all stress tests, assigns a "Sovereign Stability Score," and generates a prioritised list of hardware or logic upgrades.

## Logic & Algorithm
- **Vulnerability Mapping**: Correlates different stress test failures to find "Common Nodes" (e.g., one database being the bottleneck for 3 different tests).
- **Scoring Engine**: Calculates a weighted score based on MTTR, Data Integrity, and Cost of Failover.
- **Upgrade Synthesis**: Suggests specific infra changes (e.g., "Add 32GB RAM to the Historian node") based on the test data.

## Inputs & Outputs
- **Inputs**:
  - `all_stress_test_results` (List).
- **Outputs**:
  - `stability_scorecard` (JSON): The official "Hardness" rating of the OS.

## Acceptance Criteria
- Provide a clear, actionable "Upgrade Path" for any Stability Score < 90%.
- Maintain a historical log of stability improvements over time.
