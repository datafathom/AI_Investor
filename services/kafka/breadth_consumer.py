"""
Market Breadth Consumer.
Consumes market breadth data from Kafka.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BreadthConsumer:
    """Consumes market breadth events."""
    
    def process_message(self, topic: str, message: Dict[str, Any]):
        if topic == "market_breadth":
            advancers = message.get("advancers", 0)
            decliners = message.get("decliners", 0)
            ratio = advancers / decliners if decliners > 0 else 0
            
            logger.info(f"BREADTH_UPDATE: A/D Ratio: {ratio:.2f}")
            # In real app: Update database or cache for frontend
