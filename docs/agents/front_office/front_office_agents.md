# Front Office Department Agents (`front_office/front_office_agents.py`)

The Front Office department acts as the "Administrative HQ," managing the CEO's (user's) focus and protecting them from technical and administrative noise.

## Inbox Gatekeeper Agent (Agent 14.1)
### Description
The `InboxGatekeeperAgent` is the digital assistant that triages incoming communications. It ensures that only critical, actionable items reach the user's primary "Heads-Up Display" (HUD).

### Role
Acts as the "Noise Shield" for the CEO.

### Integration
- **Inbox Service**: Syncs with emails and messages.
- **Classification**: Uses LLM-based triage to categorize items as `NOISE`, `ACTIONABLE`, or `FYI`.
- **Urgency Scoring**: Items with an urgency score of 7+ and classified as `ACTIONABLE` are promoted to the HUD.
- **Archiving**: Non-critical items are automatically archived with the triage metadata for later review.
