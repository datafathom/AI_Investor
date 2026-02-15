# KYC/AML Compliance Agent (Agent 11.3)

## ID: `kyc_aml_compliance_agent`

## Role & Objective
The 'Verifier'. Performs Know Your Customer (KYC) and Anti-Money Laundering (AML) checks for all new counterparties, lenders, or investment partners.

## Logic & Algorithm
- **Screening**: Checks names and entities against global OFAC and PEP (Politically Exposed Persons) watchlists.
- **Due Diligence**: Aggregates public data on institutional partners to verify their legal standing.
- **Risk Scoring**: Assigns a "Counterparty Risk" score that determines the level of manual review required before a partnership.

## Inputs & Outputs
- **Inputs**:
  - `partner_details` (Dict): Entity names, EINs, or individual IDs.
- **Outputs**:
  - `aml_clearance_status` (Pass/Fail): Regulatory approval status.

## Acceptance Criteria
- Screen 100% of new financial counterparties against global watchlists before any fund movement.
- Maintain an audit trail of 100% of screening results for regulatory inquiry.
