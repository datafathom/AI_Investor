
import logging
import requests
import json
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class AlertService:
    """
    Service for dispatching internal system alerts to Slack/PagerDuty.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlertService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        sm = get_secret_manager()
        self._slack_webhook = sm.get_secret('SLACK_WEBHOOK_URL')
        self._pd_routing_key = sm.get_secret('PAGERDUTY_ROUTING_KEY')

    def trigger_alert(self, summary: str, description: str, severity: str = 'warning'):
        """
        Triggers an alert manually from application code.
        """
        logger.warning(f"Internal Alert Triggered: {summary} - {description}")
        
        if self._slack_webhook:
            try:
                payload = {
                    "text": f"🚨 *{severity.upper()} ALERT: {summary}*\n{description}"
                }
                print(f"TRACING_ALERT: {payload['text']}")
                requests.post(self._slack_webhook, json=payload, timeout=5)
            except Exception as e:
                logger.error(f"Failed to send Slack alert: {e}")

        # PagerDuty integration would go here if configured
        if self._pd_routing_key and severity == 'critical':
             logger.info("PagerDuty alert would be sent here.")

def get_alert_service() -> AlertService:
    return AlertService()
