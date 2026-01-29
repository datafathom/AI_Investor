import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TimeToExitCalculator:
    """Estimates days to convert assets to cash across market conditions."""
    
    BASE_DAYS = {
        "REIT": 2,
        "SINGLE_FAMILY": 60,
        "VACANT_LAND": 180,
        "APARTMENT_COMPLEX": 120
    }

    def estimate_exit_days(self, asset_class: str, market_condition: str = "NORMAL") -> int:
        base = self.BASE_DAYS.get(asset_class.upper(), 30)
        
        multiplier = 1.0
        if market_condition.upper() == "CRISIS": multiplier = 3.0
        elif market_condition.upper() == "BULL": multiplier = 0.5
        
        total_days = int(base * multiplier)
        logger.info(f"RE_LOG: Estimated exit for {asset_class} in {market_condition} market: {total_days} days.")
        
        return total_days
