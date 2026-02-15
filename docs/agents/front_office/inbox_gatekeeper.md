# Inbox Gatekeeper (Agent 14.1)

## ID: `inbox_gatekeeper`

## Role & Objective
The 'Digital Bouncer'. Screens all incoming emails and messages, surfacing only high-priority or time-sensitive items while filtering out noise and low-value solicitations.

## Logic & Algorithm
- **Semantic Filtering**: Uses LLM-based intent analysis to determine if an email requires an "Action," a "Read," or is "Spam."
- **Priority Scoring**: Ranks valid messages based on sender status (Partners > Family > Service Providers > Others) and deadline proximity.
- **Auto-Reply**: Drafts "Standard Response" templates for routine inquiries (e.g., meeting requests) for the user to approve.

## Inputs & Outputs
- **Inputs**:
  - `incoming_message_stream` (Emails, DMs, Slack).
- **Outputs**:
  - `curated_inbox_feed` (List): Only the messages the user actually needs to see.
  - `draft_replies` (Dict): Proposed responses for high-probability intents.

## Acceptance Criteria
- Reduce the user's "Primary Inbox" volume by 80% through effective filtering.
- Flag 100% of "Legal" or "Urgent Financial" alerts within 5 minutes of receipt.
