# Backend Service: Communication

## Overview
The **Communication Service** is the platform's multi-channel notification and alert orchestration layer. It manages outgoing messages through diverse channels including Email (Professional and Personal), Discord Webhooks, and SMS, ensuring critical financial signals reach the user with high reliability and appropriate urgency.

## Core Dispatchers

### 1. Unified Email Service (`email_service.py`)
A production-ready engine with support for multiple high-deliverability providers.
- **Provider Agnostic**: Supports **SendGrid**, **AWS SES**, and standard **SMTP**.
- **Transactional Framework**: Includes a template engine for automated workflows like "Welcome" series, "Password Reset," and "Onboarding Completion."

### 2. Gmail Specialized Client (`gmail_service.py`)
A dedicated interface for the user's personal Google account.
- **Advanced Quota Management**: Tracks daily send counts and enforces rate limits (e.g., 500 emails/day) to protect the user's Gmail reputation.
- **Rich Media Support**: Handles MIME-encoded messages with HTML bodies and attachments for daily portfolio reports.

### 3. Discord Alerting (`discord_webhook.py`)
Direct integration for high-speed trading signals and community alerts.
- **Signal Templates**: Includes specialized formatting for `AI TRADE SIGNALS` with color-coded "BUY/SELL" embeds, confidence scores, and price triggers.
- **Rich Embeds**: Uses Discord's embed system to provide detailed "footer" metadata and timestamping for audit trails.

### 4. Notification Hub & Router (`notification_manager.py`)
The intelligent logic layer that determines *how* and *where* a message is delivered based on its priority.
- **Priority Routing Matrix**:
    - **CRITICAL**: Dispatched via SMS, Push, Email, and System Console for maximum visibility.
    - **WARNING**: Sent via Push and Email.
    - **INFO**: Logged to the internal dashboard and console only.

## Dependencies
- `sendgrid` / `boto3`: Underlying API drivers for professional email providers.
- `google-api-python-client`: Powers the personal Gmail integration.
- `smtplib`: Standard Python library for SMTP fallback.

## Usage Examples

### Dispatching a Managed Alert
```python
from services.communication.notification_manager import get_notification_manager, AlertPriority

notifier = get_notification_manager()

# This will trigger SMS, Push, and Email based on CRITICAL priority
notifier.send_alert(
    message="RISK ALERT: Portfolio volatility exceeded 2.5% threshold.",
    priority=AlertPriority.CRITICAL
)
```

### Sending a Trade Signal to Discord
```python
from services.communication.discord_webhook import get_discord_webhook

webhook = get_discord_webhook(url="https://discord.com/api/webhooks/...")

await webhook.send_trade_signal(
    ticker="NVDA",
    side="buy",
    price=650.25,
    confidence=0.88
)
```
