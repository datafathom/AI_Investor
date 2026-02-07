# Backend Service: Notifications (Omnichannel Dispatch)

## Overview
The **Notifications Service** manages the outbound communication layer of the Sovereign OS. It abstracts away the complexity of integrating with various providers (Slack, Twilio, SendGrid, PagerDuty), allowing other services to simply "send a message" without worrying about the delivery mechanism. It also enforces user preferences, ensuring that alerts are delivered to the right device at the right time.

## Core Components

### 1. Preference Manager (`notification_preferences.py`)
The user control plane.
- **Channel Opt-In**: Manages the `enabled/disabled` state for each channel (SMS, Email, Slack).
- **Verification**: Handles the "Verify Phone Number" OTP flow to prevent spam.

### 2. FOMO Alert Engine (`fomo_alert.py`)
Urgency driver for deal flow.
- **Scarcity Logic**: Monitors "remaining capacity" in private deals. When allocation drops below a threshold, it triggers high-priority alerts to TIER_1 and TIER_2 clients to drive immediate action.

### 3. Provider Adapters (`slack_service.py`, `twilio_service.py`, etc.)
The delivery infrastructure.
- **Unified Interface**: Each adapter implements a standard `send()` method, allowing the calling service to be agnostic of the underlying API.
- **Mock Mode**: The `SlackClient` includes a simulation mode for development, allowing devs to see "fake" messages in the logs without spamming real channels.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings** | SMS Config | `notification_preferences.update_sms_preferences()` | **Implemented** (`SMSSettings.jsx`) |
| **Settings** | Discord/Slack Config | `slack_service.get_channels()` | **Implemented** (`DiscordSettings.jsx`) |
| **Deal Room** | Capacity Alert Badge | `fomo_alert` (triggered via socket) | **Partial** |

## Dependencies
- `twilio`: SMS and Voice API client.
- `sendgrid`: Transactional Email API client.
- `slack_sdk`: (Future) Official Slack client.

## Usage Examples

### Configuring User Preferences
```python
from services.notifications.notification_preferences import get_notification_preferences

prefs = get_notification_preferences()

# Enable SMS for "Margin Calls" only
prefs.update_sms_preferences(
    enabled=True,
    phone="+15550199",
    alert_types=["margin_call", "liquidation"]
)
```

### Triggering a Deal Scarcity Alert (FOMO)
```python
from services.notifications.fomo_alert import FOMOAlertService

fomo = FOMOAlertService()

# Push alert to TIER_1 SFO clients
fomo.push_scarcity_alert(
    deal_name="SpaceX Secondary Series N",
    remaining_capacity=500000.00, # $500k left
    recipient_tier="TIER_1_SFO"
)
```
