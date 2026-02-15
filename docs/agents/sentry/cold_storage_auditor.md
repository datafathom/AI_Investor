# Cold Storage Auditor (Agent 8.4)

## ID: `cold_storage_auditor`

## Role & Objective
The 'Governance Auditor'. Ensures all code changes and trade activities follow pre-defined SEC and departmental rules, specifically focusing on the integrity of air-gapped or restricted assets.

## Logic & Algorithm
- **Integrity Checking**: Verifies checksums of offline data backups and cold wallet transaction history.
- **Compliance Mapping**: Checks every outbound trade against a "Restricted List" of assets.
- **Air-Gap Verification**: Monitors the "Hardware Bridge" to ensure cold wallets are only connected during authorized signing sessions.

## Inputs & Outputs
- **Inputs**:
  - `checksum_registry` (List): Hashes of critical data assets.
  - `compliance_policy` (Rules): SEC and internal trading constraints.
- **Outputs**:
  - `integrity_score` (float): Confirmation that historical data hasn't been tampered with.

## Acceptance Criteria
- Detect any unauthorized modification to historical audit logs within 1 second.
- Block 100% of trades that violate the internal "Cold Storage Only" asset list.
