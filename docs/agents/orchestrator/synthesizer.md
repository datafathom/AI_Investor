# Synthesizer (Agent 1.1)

## ID: `synthesizer`

## Role & Objective
The central intelligence aggregator of the Sovereign OS. The Synthesizer is responsible for distilling thousands of granular agent logs and system events into a high-fidelity executive summary for the user.

## Logic & Algorithm
1. **Log Aggregation**: Ingests `agent.log` events from all 108 agents.
2. **Ledger Validation**: Compares internal briefing totals with the absolute truth stored in the Postgres ledger.
3. **Conflict Mapping**: Identifies divergent signals between departments (e.g., Strategist vs Trader) and queues them for resolution.
4. **Briefing Generation**: Synthesizes a daily Markdown report with cryptographic integrity checks.

## Inputs & Outputs
- **Inputs**: 
  - Kafka Activity Streams
  - Postgres Ledger Snapshots
  - Neo4j Relationship Data
- **Outputs**:
  - Daily Strategic Briefing (Markdown)
  - Conflict Resolution Queue (JSON)

## Acceptance Criteria
- Daily briefing totals must match the Postgres ledger to within 0.01% variance.
- Briefing generation must complete in under 5 seconds for a 24-hour log window.
