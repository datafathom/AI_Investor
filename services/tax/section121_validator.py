
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Section121Validator:
    """
    Validates IRS Section 121 Primary Residence exclusion.
    $250k single / $500k married exclusion on capital gains.
    """
    
    SINGLE_EXCLUSION = Decimal('250000.00')
    MARRIED_EXCLUSION = Decimal('500000.00')
    
    def validate_exclusion(
        self,
        total_gain: Decimal,
        filing_status: str,  # 'SINGLE' or 'MARRIED'
        lived_in_2_of_5_years: bool,
        is_primary_residence: bool
    ) -> Dict[str, Any]:
        """
        Calculates how much of the gain is tax-free.
        """
        max_exclusion = self.SINGLE_EXCLUSION if filing_status == 'SINGLE' else self.MARRIED_EXCLUSION
        
        qualified = lived_in_2_of_5_years and is_primary_residence
        
        applied_exclusion = Decimal('0.00')
        taxable_gain = total_gain
        
        if qualified:
            applied_exclusion = min(total_gain, max_exclusion)
            taxable_gain = total_gain - applied_exclusion
            
        logger.info(f"Section 121: Gain=${total_gain}, Status={filing_status}, ExclusionApplied=${applied_exclusion}, Qualified={qualified}")
        
        return {
            "total_gain": total_gain,
            "exclusion_qualified": qualified,
            "exclusion_applied": applied_exclusion,
            "taxable_gain_remaining": taxable_gain
        }
