
import logging
from decimal import Decimal
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CRTDeductionCalculator:
    """
    Calculates the charitable income tax deduction for a CRT.
    The remainder interest must be at least 10% of the initial value.
    Uses IRS 7520 rates.
    """
    
    def calculate_deduction(
        self,
        principal: Decimal,
        payout_rate: Decimal,
        term_years: int,
        irs_7520_rate: Decimal,
        payout_frequency: int = 1  # 1 for annual, 4 for quarterly, 12 for monthly
    ) -> Dict[str, Any]:
        """
        Simplified PV calculation for the remainder interest.
        PV = Principal * (1 / (1 + r)^n) roughly, but for CRTs it's more complex
        due to the payout stream.
        """
        
        # simplified annuity factor for demonstration of the logic
        # In production, this would use the IRS Actuarial Tables (Table U or Table B)
        r = irs_7520_rate
        n = term_years
        
        # Payout amount
        payout = principal * payout_rate
        
        # Present Value of the lifetime/term income stream (Annuity)
        # PV_annuity = Payout * [(1 - (1 + r)^-n) / r]
        if r > 0:
            pv_annuity = payout * ((1 - (1 + r)**-n) / r)
        else:
            pv_annuity = payout * Decimal(str(n))
            
        # Remainder = Principal - PV_annuity
        remainder_pv = principal - pv_annuity
        
        # 10% Rule Check
        ten_percent_rule = remainder_pv >= (principal * Decimal('0.10'))
        
        logger.info(f"CRT Deduction: Principal=${principal}, RemainderPV=${remainder_pv}, 10%Rule={ten_percent_rule}")
        
        return {
            "principal": principal,
            "term_years": n,
            "irs_7520_rate": r,
            "remainder_pv": remainder_pv.quantize(Decimal('0.01')),
            "deduction_amount": remainder_pv.quantize(Decimal('0.01')),
            "meets_10_percent_rule": ten_percent_rule
        }
