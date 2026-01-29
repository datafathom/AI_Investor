import logging
import json
from typing import Dict, Any
from services.funds.flow_processor import FlowProcessor

logger = logging.getLogger(__name__)

class PassiveFlowConsumer:
    """Consumes daily passive fund flow telemetry."""
    
    def __init__(self, kafka_config: Dict[str, Any]):
        self.config = kafka_config
        self.processor = FlowProcessor()
        self.is_running = False

    def process_message(self, message: str):
        try:
            data = json.loads(message)
            ticker = data.get("ticker")
            net_flow = data.get("net_flow_usd", 0.0)
            
            logger.info(f"KAFKA_FLOW: Processing {ticker} net_flow=${net_flow:,.2f}")
            results = self.processor.process_flow(data)
            
            if results.get("significant_outflow"):
                logger.warning(f"FLOW_ALERT: Significant redemption detected in {ticker}")
                
        except Exception as e:
            logger.error(f"KAFKA_FLOW_ERROR: {e}")

    def start(self):
        self.is_running = True
        logger.info("KAFKA_FLOW: Consumer active.")

    def stop(self):
        self.is_running = False
        logger.info("KAFKA_FLOW: Consumer stopped.")
