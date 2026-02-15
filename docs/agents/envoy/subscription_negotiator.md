# Subscription Negotiator (Agent 13.2)

## ID: `subscription_negotiator`

## Role & Objective
The 'Cost Cutter'. Identifies overlapping digital subscriptions and proactively negotiates institutional or volume pricing for high-cost data feeds.

## Logic & Algorithm
- **Arbitrage Detection**: Compares the cost of individual individual seats versus family or enterprise plans for specialized tools.
- **Negotiation Trigger**: Flags subscriptions that have been active for > 12 months for a "Retention Discount" inquiry.
- **Redundancy Audit**: Works with the Procurement Bot to identify if two different services are providing the same data (e.g., Bloomberg vs Refinitiv).

## Inputs & Outputs
- **Inputs**:
  - `recurring_billing_stream` (Data): Ongoing software and data costs.
- **Outputs**:
  - `negotiation_scripts` (str): Proposed prompts for the user to use with support teams.
  - `savings_projection` (float): Potential annual recovery.

## Acceptance Criteria
- Identify at least 3 subscription consolidation opportunities per year.
- Reduce total SaaS overhead by 15% through proactive plan tiering.
