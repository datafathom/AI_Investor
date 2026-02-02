import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PrivacyScorer:
    """
    Phase 169.5: SFO vs. MFO Privacy Advantage Score.
    Quantifies the 'Stealth Wealth' advantage of single family offices.
    """
    
    def calculate_privacy_score(self, office_type: str, uses_third_party_custodian: bool, public_filings_required: bool) -> Dict[str, Any]:
        """
        Score: 0-100. Lower is more public; higher is more private.
        """
        score = 50.0
        
        if office_type.upper() == "SFO":
            score += 20.0 # SFOs have fewer disclosure requirements
        else:
            score -= 10.0 # MFOs (RIAs) have Form ADV/etc
            
        if not uses_third_party_custodian:
            score += 15.0 # In-house custody (private keys)
            
        if not public_filings_required:
            score += 15.0 # No 13F requirements
            
        logger.info(f"ANALYSIS_LOG: {office_type} Privacy Score: {score}/100")
        
        return {
            "office_type": office_type,
            "privacy_score": score,
            "rating": "ELITE_PRIVACY" if score >= 85 else "MODERATE"
        }
