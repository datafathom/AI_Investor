import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EstateExclusionAnalyzer:
    """Analyzes asset exclusion from taxable estate based on trust status."""
    
    ESTATE_TAX_THRESHOLD_2024 = 13610000 # $13.61M per person

    def analyze_exclusion(self, market_value: float, trust_type: str, is_titled: bool) -> Dict[str, Any]:
        """
        Policy: 
        - Assets in IRREVOCABLE trusts are excluded IF correctly titled.
        - Assets in REVOCABLE trusts are INCLUDED in taxable estate.
        """
        t_type = trust_type.upper()
        
        # Must be Irrevocable AND funded (titled correctly) to be excluded
        is_excluded = (t_type == "IRREVOCABLE") and is_titled
        
        excluded_amount = market_value if is_excluded else 0.0
        taxable_amount = market_value if not is_excluded else 0.0
        
        logger.info(f"TAX_LOG: Estate Analysis: ${excluded_amount:,.2f} Excluded, ${taxable_amount:,.2f} Taxable (Trust: {trust_type}, Funded: {is_titled})")
        
        return {
            "is_excluded": is_excluded,
            "excluded_amount": round(float(excluded_amount), 2),
            "taxable_amount": round(float(taxable_amount), 2),
            "probate_status": "AVOIDED" if is_titled else "EXPOSED_TO_PROBATE"
        }
