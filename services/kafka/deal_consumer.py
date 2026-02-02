import logging
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DealConsumer:
    """
    Phase 166.1: Kafka Syndication Deal Ingestion.
    Listens for new deal opportunities on the 'SYNDICATION_LEADS' topic.
    """
    
    def __init__(self, kafka_client=None):
        self.client = kafka_client
        logger.info("DealConsumer initialized")

    def process_message(self, message: Dict[str, Any]):
        """
        Normalizes deal data and stores in Deal Flow list.
        """
        deal_id = message.get("id")
        sponsor = message.get("sponsor")
        target_irr = message.get("target_irr")
        
        logger.info(f"KAFKA_LOG: [SYNDICATION_LEADS] New Deal: {deal_id} by {sponsor} (Target IRR: {target_irr}%)")
        
        # In real, this would trigger 506(b) check and then notify eligible LPs
        return True
