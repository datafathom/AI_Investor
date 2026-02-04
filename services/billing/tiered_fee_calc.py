import logging
from typing import Dict, Any
from schemas.fee_billing import FeeSchedule

logger = logging.getLogger(__name__)

class TieredFeeCalculator:
    """Calculates AUM fees using a declining-balance tiered schedule."""
    
    def calculate_annual_fee(self, aum: float, schedule: FeeSchedule) -> float:
        total_fee = 0.0
        remaining_aum = aum
        
        # Tier 1
        t1_amount = min(remaining_aum, schedule.tier_1_max)
        total_fee += t1_amount * schedule.tier_1_rate
        remaining_aum -= t1_amount
        
        # Tier 2
        if remaining_aum > 0:
            t2_cap = schedule.tier_2_max - schedule.tier_1_max
            t2_amount = min(remaining_aum, t2_cap)
            total_fee += t2_amount * schedule.tier_2_rate
            remaining_aum -= t2_amount
            
        # Tier 3
        if remaining_aum > 0:
            total_fee += remaining_aum * schedule.tier_3_rate
            
        logger.info(f"BILLING_LOG: Calculated annual fee of ${total_fee:,.2f} on ${aum:,.2f} AUM.")
        return round(total_fee, 2)
