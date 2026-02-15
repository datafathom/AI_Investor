# Fraud Watchman (Agent 10.4)

## ID: `fraud_watchman`

## Role & Objective
The 'Zero-Trust Auditor'. Inspects every transaction for signs of card theft, unusual merchant behavior, or unauthorized institutional access.

## Logic & Algorithm
- **Anomalous Spend Detection**: Flags transactions that occur in unusual geographies or categories (e.g., a jewelry purchase in a city the user isn't in).
- **Merchant Auditing**: Cross-references merchant IDs against "High-Risk" blacklists.
- **Alert Escalation**: Triggers the Sentry department to lock credit cards if high-confidence fraud is detected.

## Inputs & Outputs
- **Inputs**:
  - `transaction_meta_data` (Dict): Merchant, location, and device ID for every spend event.
- **Outputs**:
  - `fraud_score` (0-100): Probability of malicious activity.

## Acceptance Criteria
- Detect 90% of out-of-pattern spending within 60 seconds of the transaction.
- Maintain a "False Positive" rate of < 2% to avoid user friction.
