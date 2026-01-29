import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HEMSValidator:
    """Validates trust distributions against the IRS 'HEMS' standard."""
    
    # Health, Education, Maintenance, Support
    QUALIFIED_KEYWORDS = {
        "HEALTH": ["MEDICAL", "SURGERY", "THERAPY", "DENTAL", "INSURANCE"],
        "EDUCATION": ["TUITION", "BOOKS", "ENROLLMENT", "STUDY_ABROAD"],
        "MAINTENANCE": ["RENT", "MORTGAGE", "UTILITIES", "FOOD"],
        "SUPPORT": ["CLOTHING", "BASIC_TRANSPORT", "CHILD_CARE"]
    }

    def validate_payout(self, purpose: str, amount: float) -> Dict[str, Any]:
        """
        Policy: If purpose aligns with HEMS, distribution doesn't trigger estate inclusion.
        """
        p_upper = purpose.upper()
        
        is_qualified = False
        category_found = "NONE"
        
        for category, keywords in self.QUALIFIED_KEYWORDS.items():
            if p_upper in keywords or p_upper == category:
                is_qualified = True
                category_found = category
                break
                
        if not is_qualified:
            logger.warning(f"LEGAL_ALERT: Non-HEMS distribution request: {purpose} (${amount:,.2f}). Risk of estate inclusion.")
            
        return {
            "is_hems_qualified": is_qualified,
            "category": category_found,
            "standard_status": "QUALIFIED" if is_qualified else "DISCRETIONARY_POWERS_REQUIRED"
        }
