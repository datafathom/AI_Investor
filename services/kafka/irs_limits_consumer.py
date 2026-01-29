import logging
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class IRSLimitsConsumer:
    """Consumes annual IRS contribution limit updates."""
    
    def __init__(self, kafka_config: Dict[str, Any]):
        self.config = kafka_config
        self.latest_limits = {
            "2025": {"401k": 23500, "ira": 7000, "catchup_401k": 7500},
            "2026": {"401k": 24000, "ira": 7500, "catchup_401k": 8000}
        }

    def process_message(self, message: str):
        try:
            data = json.loads(message)
            year = str(data.get("year"))
            limits = data.get("limits")
            
            self.latest_limits[year] = limits
            logger.info(f"IRS_LIMITS: Updated limits for {year}: {limits}")
            
        except Exception as e:
            logger.error(f"IRS_LIMITS_ERROR: {e}")
