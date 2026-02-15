# Robustness Scorer (Agent 16.6)

## ID: `robustness_scorer`

## Role & Objective
The 'Sanity Checker'. Ensures that after a fault is cleared (e.g., a container restarts), the system state is 100% consistent with the pre-fault period and no "Ghost State" remains.

## Logic & Algorithm
- **State Checksumming**: Compares a pre-test "State Snapshot" against a post-recovery "State Snapshot."
- **Ghost Detection**: Scans for "Orphaned Transactions" or "Zombies processes" that should have been cleaned up during recovery.
- **Database Consistency Audit**: Performs deep-level foreign key and constraint checks to ensure the ACID properties held during chaos.

## Inputs & Outputs
- **Inputs**:
  - `pre_fault_snapshot` (Data).
  - `post_recovery_snapshot` (Data).
- **Outputs**:
  - `consistency_audit_status` (Pass/Fail): Does the system really "Recover" or just restart?

## Acceptance Criteria
- Identify even a 1-bit discrepancy between pre-fault and post-recovery persistent state.
- Ensure 100% cleanup of temporary resources within 10 minutes of test completion.
