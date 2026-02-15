# Timeline Curator (Agent 15.6)

## ID: `timeline_curator`

## Role & Objective
The 'Dementia Guard'. Decides which low-value logs (e.g., routine heartbeat signals) can be safely deleted or summarized to prevent "Context Bloat" and storage waste.

## Logic & Algorithm
- **Importance Scoring**: Ranks logs based on their relevance to future "Decision Replay" or "Forensic Audits."
- **Summarization**: Collapses 1,000 "Normal" events into a single "Routine Heartbeat" summary node.
- **Garbage Collection**: Deletes ephemeral files and temporary scratchpads that have no historical value.

## Inputs & Outputs
- **Inputs**:
  - `archive_volume_metrics` (Data): Current storage utilization.
  - `log_access_frequency` (Data): How often a history segment is retrieved.
- **Outputs**:
  - `deletion_manifest` (List): IDs of nodes to be purged.

## Acceptance Criteria
- Maintain a total system log footprint below the user-defined hardware limits without losing "Significant" events.
- Summarize 90% of routine health-check logs into 1% of the original storage space.
