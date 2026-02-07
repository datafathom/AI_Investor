# Backend Service: Journaling (Real-Time Behavioral)

## Overview
The **Journaling (Real-Time Behavioral) Service** is the platform's qualitative event-capture layer. Unlike the trade-focused `Journal` service, this service focuses on the **Present State** of the user. It logs emotional triggers, captured sentiment, and instances where system guardrails have intervened to prevent impulsive or sub-optimal decisions. This data is critical for building a longitudinal map of a user's psychological relationship with their assets.

## Core Components

### 1. Behavioral Log Engine (`behavioral_log.py`)
The high-fidelity recorder for human-system interaction.
- **Event Journaling**: Captures specific behavioral events (e.g., "Impulse Buy Attempt", "Panic Sell Blocked", "Revenge Trade Flagged") with detailed qualitative context.
- **Sentiment Tracking**: Assigns a numeric **Sentiment Score** to each event, allowing the system's behavioral agents to monitor for patterns of emotional distress or over-excitement that could lead to financial risk.
- **Intervention Ledger**: Maintains a permanent record of every time a "Prevented Trade" was triggered by the platform's risk or behavioral layers, allowing for subsequent post-mortem analysis.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Psychology Hub** | Emotional Sentiment Pulse | `behavioral_log.log_event()` |
| **Psychology Hub** | Intervention History Ticker| `behavioral_log.get_recent_logs()` |
| **Whale Watch Terminal** | User Stability Meter | `behavioral_log` (Sentiment aggregate) |
| **Admin Station** | Behavioral Audit Ledger | `behavioral_log.logs` |

## Dependencies
- `datetime`: Provides ISO-standard timestamps for event traceability.
- `logging`: Mirrors behavioral events to the system logs for cross-referencing with trade execution errors.

## Usage Examples

### Logging an Impulsive Execution Attempt
```python
from services.journaling.behavioral_log import BehavioralLog

log_svc = BehavioralLog()

# Capture an event where the user tried to FOMO into a volatile crypto asset
log_svc.log_event(
    event_type="FOMO_GUARD_TRIGGERED",
    details="User attempted to buy DOGE after 40% spike. Execution blocked by Behavioral Guardrail.",
    sentiment_score=-8 # High emotional intensity / Low rational score
)

print(f"Logged {len(log_svc.logs)} behavioral events.")
```

### Retrieving Recent Tactical Interventions
```python
from services.journaling.behavioral_log import BehavioralLog

log_svc = BehavioralLog()

# (Simulated) Fetching the last 5 interventions for the 'Intervention History' widget
interventions = log_svc.get_recent_logs(limit=5)

for entry in interventions:
    print(f"[{entry['timestamp']}] {entry['type']}: {entry['details']}")
```
