# Credit Score Sentinel (Agent 10.6)

## ID: `credit_score_sentinel`

## Role & Objective
The 'FICO Guardian'. Monitors credit reports and flags any unauthorized applications, score changes, or reporting errors across the three major bureaus.

## Logic & Algorithm
- **Soft-Pull Monitoring**: Regularly checks Credit Karma or equivalent APIs for changes in the credit profile.
- **Inquiry Alert**: Immediately flags new "Hard Inquiries" to ensure they were authorized by the user.
- **Optimization Advice**: Recommends timing for credit card payments to optimize "Utilization Ratios" before a reporting cycle.

## Inputs & Outputs
- **Inputs**:
  - `credit_report_data` (Dict): Inquiries, balances, and scores.
- **Outputs**:
  - `credit_health_score` (int): Combined FICO/Vantage estimate.
  - `alert_log` (List): Critical changes to the credit file.

## Acceptance Criteria
- Notify the user of any 20-point score drop within 24 hours of reporting.
- Identify 100% of hard inquiries and link them to known financial actions (e.g. mortgage application).
