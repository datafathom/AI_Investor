# Backend Service: Calendar

## Overview
The **Calendar Service** serves as the system's temporal orchestration layer. It bridges the gap between raw market event data (earnings calls, dividend dates) and the user's personal scheduling tools, providing a unified, color-coded timeline for financial awareness and decision-making.

## Core Components

### 1. Google Calendar Integration (`google_calendar_service.py`)
A comprehensive wrapper for the Google Calendar v3 API.
- **Visual Categorization**: Automatically applies internal color coding to events:
    - **Blue (ID 9)**: Corporate Earnings.
    - **Green (ID 10)**: Dividend Payments.
    - **Yellow (ID 5)**: Portfolio Rebalancing.
- **Intelligent Reminders**: Configures multi-channel alerts (e.g., Email 24 hours prior, Popup 1 hour prior) for all financial milestones.
- **CRUD Lifecycle**: Full support for creating, listing, updating, and asynchronously deleting calendar events across any user-authorized Google Calendar.

### 2. Earnings & Dividend Sync (`earnings_sync.py`)
An automated pipeline that monitors the user's investment universe.
- **AlphaVantage Integration**: Periodically fetches global earnings and dividend calendars.
- **Holdings Filtering**: Cross-references the global calendar against the user's real-time portfolio holdings to isolate relevant events.
- **Sync Logic**: Creates high-visibility events on the user's calendar with detailed descriptions, including **Estimated EPS** and conference call links where available. It includes a de-duplication mechanism to ensure the calendar remains clean across multiple sync cycles.

## Dependencies
- `google-api-python-client`: Powers the underlying Google Calendar API communication.
- `services.data.alpha_vantage`: Source of corporate financial event data.
- `services.system.secret_manager`: Manages OAuth2 credentials and user access tokens safely.

## Usage Examples

### Syncing Earnings for a User's Portfolio
```python
from services.calendar.earnings_sync import get_earnings_sync_service

sync_service = get_earnings_sync_service()

# holdings = ["AAPL", "TSLA", "NVDA"]
stats = await sync_service.sync_earnings_for_user(
    user_id="user_vanguard_1",
    access_token="YA29.GLC...", # OAuth token from Auth service
    holdings=my_holdings,
    days_ahead=90
)

print(f"Calendar Sync Success. Created {stats['events_created']} new events.")
```

### Manually Creating a Rebalancing Reminder
```python
from services.calendar.google_calendar_service import get_calendar_service
from datetime import datetime, timedelta

cal = get_calendar_service()

await cal.create_event(
    access_token="YA29.GLC...",
    title="Quarterly Portfolio Rebalance",
    description="Analyze factor exposures and adjust weights per AI Alpha engine.",
    start_time=datetime.now() + timedelta(days=7),
    event_type="rebalance"
)
```
