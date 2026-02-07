import logging
import asyncio
from typing import Any, Dict, Optional
from services.kafka.consumer import BaseConsumer, ConsumerConfig
from services.notifications.slack_service import get_slack_service

logger = logging.getLogger(__name__)

class SlackNotificationConsumer(BaseConsumer):
    """
    Consumer for outgoing Slack alerts.
    
    Listens to the 'slack.alerts' topic and delivers messages via SlackService.
    """
    
    def __init__(self, bootstrap_servers: Optional[str] = None) -> None:
        """Initialize Slack alert consumer."""
        config = ConsumerConfig(
            topics=['slack.alerts'],
            group_id='slack-alert-delivery-group'
        )
        super().__init__(config, bootstrap_servers)
        # Use a mock service if SLACK_BOT_TOKEN is missing to avoid crashes
        self.service = get_slack_service()
        logger.info("SlackNotificationConsumer initialized (Topic: slack.alerts)")

    def process_message(self, message: Dict[str, Any]) -> None:
        """Deliver Kafka alert to Slack."""
        text = message.get("text")
        if not text:
            logger.warning("Received Slack alert with no text")
            return
            
        level = message.get("level", "info")
        channel = message.get("channel")
        job_id = message.get("job_id")

        logger.info(f"📤 Kafka -> Slack | Level: {level} | Msg: {text[:50]}...")
        
        try:
            # BaseConsumer runs in a thread. We use a dedicated loop for async delivery.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.service.send_notification(
                    text=text,
                    level=level,
                    channel=channel,
                    job_id=job_id
                ))
            finally:
                loop.close()
        except Exception as e:
            logger.error(f"Failed to deliver Slack alert from Kafka: {e}")

def get_slack_consumer() -> SlackNotificationConsumer:
    """Singleton accessor for the Slack consumer."""
    return SlackNotificationConsumer()
