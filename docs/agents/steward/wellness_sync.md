# Wellness Sync (Agent 9.5)

## ID: `wellness_sync`

## Role & Objective
The 'Human Capital Monitor'. Tracks lifestyle metrics (sleep, focus, activity) that impact financial decision-making quality and long-term health benchmarks.

## Logic & Algorithm
- **Data Ingestion**: Syncs with Apple Health/Google Fit to monitor biometric stability (RHR, HRV, Sleep Duration).
- **Decision Correlation**: Cross-references "Poor Sleep" nights with "Impulsive" trades or budget breaches identified by the Auditor.
- **Lifestyle Scoring**: Provides a "Readiness" score to the Orchestrator, influencing the priority of high-stress tasks.

## Inputs & Outputs
- **Inputs**:
  - `biometric_data` (Stream): Health metrics from authorized wearables.
- **Outputs**:
  - `readiness_score` (0-100): Daily metric of cognitive and physical performance potential.

## Acceptance Criteria
- Maintain biometric data privacy by storing raw health feeds in a local, encrypted node.
- Provide a daily readiness score within 30 minutes of the user's wake event.
