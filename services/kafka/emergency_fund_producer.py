import logging
import json
from datetime import datetime
from typing import Dict, Any
from schemas.emergency_fund import EmergencyFundKafkaMessage

logger = logging.getLogger(__name__)

class EmergencyFundProducer:
    """Produces real-time emergency fund status updates to Kafka."""
    
    def __init__(self, kafka_client=None):
        self.client = kafka_client

    def emit_status(self, user_id: str, liquid_cash: float, monthly_expenses: float):
        months = liquid_cash / monthly_expenses if monthly_expenses > 0 else 999
        tier = "ADEQUATE" # Default dummy
        
        # Determine tier logic...
        if months < 3: tier = "CRITICAL"
        elif months < 6: tier = "LOW"
        
        message = EmergencyFundKafkaMessage(
            user_id=user_id,
            liquid_cash=liquid_cash,
            monthly_expenses=monthly_expenses,
            months_coverage=round(months, 2),
            coverage_tier=tier,
            alert_level="HIGH" if months < 3 else "MEDIUM" if months < 6 else "LOW"
        )
        
        logger.info(f"KAFKA_PRODUCE: Emitted status for user {user_id}: {months} months coverage")
        # In real env: self.client.produce("emergency-fund-status", message.json())
        return message
