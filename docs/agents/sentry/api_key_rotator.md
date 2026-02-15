# API Key Rotator (Agent 8.2)

## ID: `api_key_rotator`

## Role & Objective
The 'Internal Auditor'. Periodically attempts to 'hack' the system's own logic to find vulnerabilities and manages the lifecycle of all external API credentials.

## Logic & Algorithm
- **Automated Rotation**: Enforces 30-day rotation cycles for all brokerage and data provider API keys.
- **Secrets Management**: Interfaces with the encrypted vault to update environment variables across the container fleet.
- **Vulnerability Scanning**: Simulates unauthorized access attempts to verify the integrity of the Permission Auditor's gates.

## Inputs & Outputs
- **Inputs**:
  - `active_secrets_inventory` (Dict): List of service keys and their expiration dates.
- **Outputs**:
  - `rotation_status` (Success/Fail): Confirmation of key updates.
  - `vulnerability_report` (List): Identified weak points in the internal logic.

## Acceptance Criteria
- 100% of external API keys must be rotated without service downtime.
- New credentials must be propagated to all microservices within 10 seconds of creation.
