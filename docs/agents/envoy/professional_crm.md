# Professional CRM (Agent 13.5)

## ID: `professional_crm`

## Role & Objective
The 'Network Manager'. Tracks every professional interaction (investors, partners, mentors) and sets reminders for strategic follow-ups.

## Logic & Algorithm
- **Interaction Logging**: Automatically scrapes calendar events and email headers to update the "Relationship Pipeline."
- **Nurture Cycles**: Flags high-value contacts that haven't been engaged in more than 6 months.
- **Context Synthesis**: Summarizes the last 3 interactions with a contact before a scheduled meeting to provide the user with "Instant Recall."

## Inputs & Outputs
- **Inputs**:
  - `calendar_feed` (Stream): Scheduled meetings and calls.
  - `email_headers` (Data): Proof of engagement.
- **Outputs**:
  - `follow_up_reminders` (List): Actionable tasks to maintain the network.

## Acceptance Criteria
- Log 100% of professional meetings with a context-rich "Last Transaction" summary.
- Alert the user to "Relationship Decay" for top-tier contacts with 100% reliability.
