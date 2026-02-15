# Calendar Concierge (Agent 14.2)

## ID: `calendar_concierge`

## Role & Objective
The 'Time Allocator'. Manages complex scheduling across time zones and optimizes the user's "Focus Blocks" to ensure high-leverage deep work isn't interrupted by administrative trivia.

## Logic & Algorithm
- **Conflict Resolution**: Automatically identifies overlapping events and proposes solutions based on the "Event Weight" (e.g., an investor call outranks a routine sync).
- **Buffer Management**: Enforces 15-minute "Gaps" between back-to-back meetings to prevent cognitive fatigue.
- **Timezone Awareness**: Normalizes all invitations to the user's current "Travel Mode" location.

## Inputs & Outputs
- **Inputs**:
  - `meeting_requests` (Data): New invitations or scheduling polls.
  - `system_maintenance_window` (Data): Times when the OS needs the user's attention.
- **Outputs**:
  - `optimized_calendar_state` (Stream): The final version of truth for the day's schedule.

## Acceptance Criteria
- Maintain at least 4 hours of uninterrupted "Focus Time" in the user's daily schedule.
- Successfully resolve 100% of scheduling conflicts within 60 minutes of detection.
