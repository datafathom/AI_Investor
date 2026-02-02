import logging
from typing import List, Dict, Any
from datetime import date

logger = logging.getLogger(__name__)

class ResidencyTimer:
    """
    Phase 184.2: 8-of-15 Years Residency Requirement Validator.
    Tracks long-term residency to trigger Covered Expatriate status under IRC 877A.
    """
    
    def calculate_residency_years(self, residency_history: List[int]) -> int:
        """
        Given a list of years the individual was a US resident, returns the count
        of years in the last 15 years.
        """
        current_year = date.today().year
        lookback_period = range(current_year - 15, current_year)
        
        resident_years_in_period = [y for y in residency_history if y in lookback_period]
        count = len(resident_years_in_period)
        
        logger.info(f"LEGAL_LOG: Residency check: {count} of last 15 years as resident.")
        return count

    def is_long_term_resident(self, residency_history: List[int]) -> bool:
        """
        Checks if the individual meets the 8-of-15 years threshold.
        """
        return self.calculate_residency_years(residency_history) >= 8

    def validate_expatriation_eligibility(self, residency_history: List[int]) -> Dict[str, Any]:
        years = self.calculate_residency_years(residency_history)
        is_ltr = years >= 8
        
        return {
            "residency_years_count": years,
            "is_long_term_resident": is_ltr,
            "subject_to_exit_tax": is_ltr,
            "status": "COVERED_RESIDENT" if is_ltr else "NON_COVERED_RESIDENT"
        }
