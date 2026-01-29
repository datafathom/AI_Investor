import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CarryEngine:
    """
    Calculates Performance Fees (Carried Interest) for alternative assets.
    Formula: Max(0, (Net_Profit - Hurdle) * Carry_Rate)
    Includes High Water Mark protection.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CarryEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("CarryEngine initialized")

    def calculate_performance_fee(
        self, 
        current_nav: Decimal, 
        previous_peak_nav: Decimal, 
        opening_nav: Decimal,
        hurdle_rate: Decimal = Decimal('0.05'),
        carry_rate: Decimal = Decimal('0.20')
    ) -> Dict[str, Any]:
        """
        Policy: No fee until High Water Mark (Peak NAV) is exceeded.
        Performance fee is only on the portion ABOVE the hurdle.
        """
        # 1. HWM Check
        if current_nav <= previous_peak_nav:
            logger.info(f"BILLING_LOG: No performance fee. Current NAV {current_nav} <= Peak {previous_peak_nav}")
            return {"fee_amount": Decimal('0.00'), "reason": "BELOW_HIGH_WATER_MARK"}
        
        # 2. Hurdle Check
        target_return = opening_nav * (Decimal('1') + hurdle_rate)
        if current_nav <= target_return:
            logger.info(f"BILLING_LOG: No performance fee. Return below hurdle of {hurdle_rate:.1%}")
            return {"fee_amount": Decimal('0.00'), "reason": "BELOW_HURDLE"}
            
        # 3. Calculate Carry
        profit_above_hurdle = current_nav - target_return
        fee = profit_above_hurdle * carry_rate
        
        logger.info(f"BILLING_LOG: ACCRUED Performance Fee: ${fee:,.2f} on ${profit_above_hurdle:,.2f} alpha.")
        
        return {
            "fee_amount": round(fee, 2),
            "basis_alpha": round(profit_above_hurdle, 2),
            "status": "ACCRUED"
        }
