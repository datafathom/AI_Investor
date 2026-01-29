import logging
import json
from typing import Dict, Any
from services.compliance.cois_calculator import COISCalculator

logger = logging.getLogger(__name__)

class COISConsumer:
    """Consumes telemetry data to trigger COIS recalculations."""
    
    def __init__(self, kafka_config: Dict[str, Any]):
        self.config = kafka_config
        self.calculator = COISCalculator()
        self.is_running = False

    def process_message(self, message: str):
        try:
            data = json.loads(message)
            event_type = data.get("event")
            
            if event_type == "REVENUE_RECEIVED" or event_type == "TRADE_EXECUTED":
                advisor_id = data.get("advisor_id")
                logger.info(f"KAFKA_COIS: Recalculating score for advisor {advisor_id} due to {event_type}")
                
                # In a real system, we'd fetch full history here
                score = self.calculator.calculate_score(data)
                
                # Persist score or emit to another topic
                logger.info(f"KAFKA_COIS: New COIS score for {advisor_id} is {score}")
        
        except Exception as e:
            logger.error(f"KAFKA_COIS_ERROR: {e}")

    def start(self):
        self.is_running = True
        logger.info("KAFKA_COIS: Consumer started.")

    def stop(self):
        self.is_running = False
        logger.info("KAFKA_COIS: Consumer stopped.")
