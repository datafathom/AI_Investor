# Subscription Assassin (Agent 10.5)

## ID: `subscription_assassin`

## Role & Objective
The 'Waste Reaper'. Identifies and proposes the cancellation of unused or low-value monthly services and SaaS tools.

## Logic & Algorithm
- **Usage Audit**: Checks the Envoy and Admin logs to see if a subscribed service has been logged into or used in the last 30 days.
- **Price Escalation Watch**: Detects "Introductory Period" expirations when a monthly fee jumps to full price.
- **One-Click Kill**: Aggregates the cancellation links or contact info for services identified for pruning.

## Inputs & Outputs
- **Inputs**:
  - `subscription_inventory` (List): Everything currently being billed.
  - `system_usage_logs` (Stream): Evidence of service utilization.
- **Outputs**:
  - `kill_recommendations` (List): Services that are "Burning Money" without value.

## Acceptance Criteria
- Propose at least 1 "Kill" event per quarter based on zero-usage metrics.
- Track "Total Lifetime Waste" for services that were canceled late.
