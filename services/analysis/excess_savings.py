"""
Excess Savings Depletion Estimator.
Forecasts when consumer stimulus cash runs out.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SavingsDepletionEst:
    """Estimates consumer savings runway."""
    
    def estimate_depletion_date(self, current_excess: float, burn_rate_monthly: float) -> str:
        if burn_rate_monthly <= 0: return "NEVER"
        
        months = current_excess / burn_rate_monthly
        depletion_date = datetime.now() + timedelta(days=int(months * 30.44))
        
        logger.info(f"CONSUMER_LOG: Excess savings estimated dry by {depletion_date.strftime('%Y-%m')}")
        return depletion_date.isoformat()
