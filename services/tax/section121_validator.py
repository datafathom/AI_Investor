"""
Section 121 Primary Residence Exclusion Validator
PURPOSE: Validate eligibility for the $250k/$500k capital gains exclusion
         on primary residence sales per IRS Section 121.
         
RULES:
1. Ownership Test: Must have owned the home for at least 2 years during 5-year period before sale
2. Use Test: Must have lived in the home as primary residence for at least 2 years
3. Look-Back Rule: Can only claim exclusion once every 2 years
"""

import logging
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Section121Result:
    """Result of Section 121 exclusion validation."""
    is_eligible: bool
    reason: str
    exclusion_amount: Decimal
    taxable_gain: Decimal
    ownership_days: int
    use_days: int


class Section121Validator:
    """
    Validates IRS Section 121 Primary Residence exclusion.
    $250k single / $500k married exclusion on capital gains.
    
    Enhanced with detailed eligibility tracking and mixed-use property support.
    """
    
    SINGLE_EXCLUSION = Decimal('250000.00')
    MARRIED_EXCLUSION = Decimal('500000.00')
    MIN_DAYS_REQUIRED = 730  # 2 years
    
    def validate_exclusion(
        self,
        total_gain: Decimal,
        filing_status: str,  # 'SINGLE' or 'MARRIED'
        lived_in_2_of_5_years: bool,
        is_primary_residence: bool
    ) -> Dict[str, Any]:
        """
        Calculates how much of the gain is tax-free (simple validation).
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

    def validate_detailed_eligibility(
        self,
        sale_date: date,
        purchase_date: date,
        primary_residence_start: date,
        primary_residence_end: date,
        last_exclusion_date: Optional[date],
        filing_status: str,
        capital_gain: Decimal
    ) -> Section121Result:
        """
        Detailed validation with ownership and use day tracking.
        """
        lookback_days = 1825  # 5 years
        lookback_start = sale_date - timedelta(days=lookback_days)
        
        # Ownership Test
        ownership_days = (sale_date - purchase_date).days
        ownership_test_met = ownership_days >= self.MIN_DAYS_REQUIRED
        
        # Use Test
        effective_start = max(primary_residence_start, lookback_start)
        effective_end = min(primary_residence_end, sale_date)
        use_days = max(0, (effective_end - effective_start).days)
        use_test_met = use_days >= self.MIN_DAYS_REQUIRED
        
        # Look-Back Rule
        lookback_clear = True
        if last_exclusion_date:
            lookback_clear = (sale_date - last_exclusion_date).days >= 730
        
        is_eligible = ownership_test_met and use_test_met and lookback_clear
        
        max_exclusion = self.MARRIED_EXCLUSION if filing_status == 'MARRIED' else self.SINGLE_EXCLUSION
        exclusion_amount = min(capital_gain, max_exclusion) if is_eligible else Decimal("0")
        taxable_gain = max(Decimal("0"), capital_gain - exclusion_amount)
        
        if is_eligible:
            reason = f"Eligible for ${exclusion_amount:,.0f} exclusion"
        elif not ownership_test_met:
            reason = f"Ownership test failed: {ownership_days} days"
        elif not use_test_met:
            reason = f"Use test failed: {use_days} days"
        else:
            reason = "2-year lookback rule not met"
        
        return Section121Result(
            is_eligible=is_eligible,
            reason=reason,
            exclusion_amount=exclusion_amount,
            taxable_gain=taxable_gain,
            ownership_days=ownership_days,
            use_days=use_days
        )

    def calculate_mixed_use_split(
        self,
        total_gain: Decimal,
        personal_use_percentage: Decimal,
        filing_status: str = "MARRIED"
    ) -> Dict[str, Any]:
        """
        Calculate tax treatment for mixed-use property (e.g., home with rental unit).
        """
        personal_gain = total_gain * personal_use_percentage
        rental_gain = total_gain * (1 - personal_use_percentage)
        
        max_exclusion = self.MARRIED_EXCLUSION if filing_status == "MARRIED" else self.SINGLE_EXCLUSION
        excluded_gain = min(personal_gain, max_exclusion)
        taxable_personal = max(Decimal("0"), personal_gain - excluded_gain)
        
        return {
            "personal_use_gain": personal_gain,
            "rental_use_gain": rental_gain,
            "section_121_exclusion": excluded_gain,
            "taxable_from_personal": taxable_personal,
            "eligible_for_1031": rental_gain
        }


# Singleton
_instance: Optional[Section121Validator] = None

def get_section121_validator() -> Section121Validator:
    global _instance
    if _instance is None:
        _instance = Section121Validator()
    return _instance

