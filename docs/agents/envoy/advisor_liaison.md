# Advisor Liaison (Agent 13.1)

## ID: `advisor_liaison`

## Role & Objective
The 'Partner Gateway'. Manages secure communication, document exchange, and data sharing with external professional partners like CPAs, lawyers, and financial advisors.

## Logic & Algorithm
- **Secure File Transfer**: Encrypts and stages tax documents or legal briefs for external retrieval.
- **Access Control**: Grants time-limited, read-only access to specific folders in the "Knowledge Base" for partner auditing.
- **Communication Threading**: Logs all emails and Slack messages with advisors to the Historian's "Institutional Memory."

## Inputs & Outputs
- **Inputs**:
  - `professional_service_requests` (List): Tasks requiring partner input.
- **Outputs**:
  - `partner_briefing_packet` (PDF): Consolidated data for the advisor's review.

## Acceptance Criteria
- Automate the delivery of quarterly tax packets to the CPA with 100% data integrity.
- Track "Last Contacted" timestamps for 100% of the flat-fee advisor list.
