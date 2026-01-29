
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """
    Monitors a beneficiary's personal accounts to ensure they stay 
    below the $2,000 resource limit for SSI/Medicaid.
    """
    
    RESOURCE_LIMIT = Decimal('2000.00')
    
    def check_eligibility_buffer(self, beneficiary_balance: Decimal) -> Dict[str, Any]:
        """
        Checks how close the beneficiary is to the resource limit.
        """
        buffer = self.RESOURCE_LIMIT - beneficiary_balance
        is_safe = buffer > 0
        
        logger.info(f"Resource Check: Balance=${beneficiary_balance}, Limit=${self.RESOURCE_LIMIT}, Safe={is_safe}")
        
        return {
            "balance": beneficiary_balance,
            "limit": self.RESOURCE_LIMIT,
            "buffer": buffer,
            "is_within_limit": is_safe,
            "recommend_action": "NONE" if buffer > Decimal('500.00') else "STOP_DISTRIBUTION" if not is_safe else "WARNING"
        }
