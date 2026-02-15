# Admin Overseer (Agent 0.1)

## ID: `admin_overseer`

## Role & Objective
The 'System Administrator'. Provides high-level oversight of all 19 departments and ensures the overall institutional health, security, and performance of the AI Investor OS.

## Logic & Algorithm
- **Departmental Pulse**: Aggregates the `primaryMetric` from all 19 departments to generate a "Total Institutional Health" score.
- **Resource Allocation**: Monitors CPU/Memory/Storage usage across all agents and microservices, triggering "Clean Build" or "Stop Process" commands if thresholds are exceeded.
- **Security Escalation**: Acts as the final authority for the Red Team Sentry and breach alerts, coordinating recovery paths.

## Inputs & Outputs
- **Inputs**:
  - `system_telemetry` (Data): Metrics from all active departments.
- **Outputs**:
  - `admin_status_report` (Dict): High-level system health and critical alerts.

## Acceptance Criteria
- Maintain system-wide uptime of 99.9%.
- Trigger institutional lockdown in < 1 second of a Level 10 breach detection.
