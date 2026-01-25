# Error Tracking & Monitoring Setup Guide

This guide explains how to set up production error tracking and monitoring for the AI Investor platform.

## Overview

The error tracking system includes:

- **Sentry**: Error tracking and performance monitoring
- **Log Aggregation**: Centralized logging (ELK, Loki, or CloudWatch)
- **Alerting**: Real-time alerts via Slack, PagerDuty, Email, SMS
- **Dashboards**: Grafana dashboards for error visualization

## Sentry Setup

### 1. Create Sentry Project

1. Go to <https://sentry.io> and create an account
2. Create a new project:
   - Platform: Python (for backend)
   - Platform: React (for frontend)
3. Copy the DSN (Data Source Name)

### 2. Configure Backend

Add to `.env.production`:

```bash
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
APP_ENV=production
APP_VERSION=1.0.0
```

### 3. Configure Frontend

Add to `frontend2/.env.production`:

```bash
VITE_SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
VITE_SENTRY_TRACES_SAMPLE_RATE=0.1
VITE_SENTRY_REPLAY_SAMPLE_RATE=0.1
```

### 4. Install Dependencies

**Backend**:

```bash
pip install sentry-sdk
```

**Frontend**:

```bash
cd frontend2
npm install @sentry/react
```

## Log Aggregation Setup

### Option 1: ELK Stack (Elasticsearch, Logstash, Kibana)

1. **Deploy ELK Stack**:

   ```bash
   docker-compose -f infra/docker-compose.logging.yml up -d
   ```

2. **Configure Logstash**:
   - Create logstash config to parse application logs
   - Forward logs from application to Elasticsearch

3. **Access Kibana**:
   - URL: <http://localhost:5601>
   - Create index patterns
   - Build dashboards

### Option 2: Loki (Grafana Loki)

1. **Deploy Loki**:

   ```bash
   docker-compose -f infra/docker-compose.loki.yml up -d
   ```

2. **Configure Promtail**:
   - Install Promtail on application servers
   - Configure to scrape application logs
   - Forward to Loki

3. **Access Grafana**:
   - URL: <http://localhost:3000>
   - Add Loki as data source
   - Create dashboards

### Option 3: AWS CloudWatch

1. **Install CloudWatch Agent**:

   ```bash
   wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
   sudo rpm -U ./amazon-cloudwatch-agent.rpm
   ```

2. **Configure Agent**:
   - Create IAM role with CloudWatch permissions
   - Configure agent to collect logs
   - Set up log groups

3. **View Logs**:
   - AWS Console → CloudWatch → Logs
   - Create metric filters
   - Set up alarms

## Alerting Setup

### Slack Integration

1. **Create Slack Webhook**:
   - Go to <https://api.slack.com/apps>
   - Create new app
   - Enable Incoming Webhooks
   - Create webhook URL

2. **Configure**:

   ```bash
   # SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

### PagerDuty Integration

1. **Create PagerDuty Service**:
   - Sign up at <https://www.pagerduty.com>
   - Create new service
   - Copy Integration Key

2. **Configure**:

   ```bash
   PAGERDUTY_ROUTING_KEY=your-routing-key
   ```

### Email Alerts

1. **Configure SendGrid**:

   ```bash
   SENDGRID_API_KEY=your-sendgrid-api-key
   ADMIN_EMAIL=admin@yourdomain.com
   ```

### SMS Alerts (Twilio)

1. **Configure Twilio**:

   ```bash
   TWILIO_ACCOUNT_SID=your-account-sid
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_FROM_NUMBER=+1234567890
   ADMIN_PHONE_NUMBER=+1234567890
   ```

## Prometheus & Grafana Setup

### 1. Deploy Prometheus

```bash
docker-compose -f infra/docker-compose.monitoring.yml up -d
```

### 2. Configure Application Metrics

The application exports metrics at `/metrics` endpoint. Prometheus will scrape these.

### 3. Import Grafana Dashboards

1. Access Grafana: <http://localhost:3000>
2. Import dashboards from `infra/grafana/dashboards/`
3. Configure data sources (Prometheus, Loki)

## Usage

### Backend Error Tracking

```python
from services.monitoring.error_tracker import get_error_tracker

error_tracker = get_error_tracker()

# Capture exception
try:
    # some code
except Exception as e:
    error_tracker.capture_exception(e)

# Capture message
error_tracker.capture_message("Something went wrong", level="error")

# Set user context
error_tracker.set_user(user_id="123", email="user@example.com")

# Add breadcrumb
error_tracker.add_breadcrumb("User clicked button", category="ui")
```

### Frontend Error Tracking

```javascript
import { captureException, captureMessage, setUser } from './utils/errorTracking';

// Capture exception
try {
  // some code
} catch (error) {
  captureException(error, { context: 'additional info' });
}

// Capture message
captureMessage('Something went wrong', 'error', { context: 'info' });

// Set user
setUser(userId, email, username);
```

### Sending Alerts

```python
from services.monitoring.alert_manager import get_alert_manager, AlertLevel

alert_manager = get_alert_manager()

# Send critical alert
alert_manager.send_alert(
    "Database connection failed",
    level=AlertLevel.CRITICAL,
    channels=['slack', 'pagerduty'],
    database='postgres',
    error_count=5
)
```

## Monitoring Best Practices

1. **Set Appropriate Alert Thresholds**:
   - Don't alert on every error
   - Use rate-based alerts (errors per minute)
   - Set different thresholds for different environments

2. **Use Alert Levels Appropriately**:
   - **CRITICAL**: Service down, data loss, security breach
   - **ERROR**: High error rate, failed transactions
   - **WARNING**: Degraded performance, approaching limits
   - **INFO**: Informational messages

3. **Avoid Alert Fatigue**:
   - Group related alerts
   - Use alert suppression
   - Set up on-call rotation

4. **Monitor Key Metrics**:
   - Error rate
   - Response time (p50, p95, p99)
   - Throughput
   - Resource usage (CPU, memory, disk)

## Troubleshooting

### Sentry Not Receiving Events

1. Check SENTRY_DSN is set correctly
2. Verify network connectivity to Sentry
3. Check Sentry project settings
4. Review application logs for Sentry errors

### Alerts Not Sending

1. Verify webhook URLs and API keys
2. Check network connectivity
3. Review alert manager logs
4. Test individual channels

### Logs Not Appearing

1. Verify log aggregation service is running
2. Check log forwarding configuration
3. Verify application is writing logs
4. Check log retention policies

## Next Steps

- [ ] Set up Sentry projects
- [ ] Configure log aggregation
- [ ] Set up alert channels
- [ ] Import Grafana dashboards
- [ ] Configure Prometheus alerts
- [ ] Test error tracking end-to-end
- [ ] Set up on-call rotation
