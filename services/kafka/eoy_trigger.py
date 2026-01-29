
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EOYHarvestTrigger:
    """
    Triggers year-end tax harvesting alerts via Kafka.
    """
    
    def check_eoy_window(self, recognized_ytd_gains: float) -> Dict[str, Any]:
        """
        Checks if the EOY harvesting alert should fire (December).
        """
        from datetime import datetime
        month = datetime.now().month
        
        if month == 12 and recognized_ytd_gains > 1000:
            logger.warning(f"EOY TAX HARVEST TRIGGER: Recognized gains of ${recognized_ytd_gains} pending offset.")
            return {
                "alert": "URGENT",
                "reason": "December Tax Loss Harvesting Window",
                "suggested_action": "EXECUTE_OFFSET_TRADES"
            }
            
        return {"alert": "NONE", "status": "MONITORING"}
