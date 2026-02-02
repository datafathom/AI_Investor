import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PassportGate:
    """
    Phase 188.1: EU Passport Logic Gate.
    Permits or denies real estate acquisitions restricted to EU citizens.
    """
    
    def verify_eu_access(self, user_passports: List[str], target_asset_country: str) -> Dict[str, Any]:
        """
        Checks if the user has a passport that grants EU accession.
        """
        # List of EU ISO codes
        EU_COUNTRIES = [
            "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", 
            "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", 
            "NL", "PL", "PT", "RO", "SE", "SI", "SK"
        ]
        
        has_eu_passport = any(p.upper() in EU_COUNTRIES for p in user_passports)
        is_eu_asset = target_asset_country.upper() in EU_COUNTRIES
        
        can_buy = not is_eu_asset or has_eu_passport
        
        logger.info(f"MOBILITY_LOG: EU Access Check for {target_asset_country}: {'ALLOWED' if can_buy else 'DENIED'}")
        
        return {
            "can_acquire": can_buy,
            "asset_requires_eu_pass": is_eu_asset,
            "user_has_eu_pass": has_eu_passport,
            "status": "PERMITTED" if can_buy else "RESTRICTED"
        }
