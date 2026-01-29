import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SOEClassifier:
    """Classifies international companies based on state control levels."""
    
    def classify_soe(self, ownership_pct: float, controlling_entity: str) -> bool:
        """
        Logic: 
        - > 50% ownership is SOE.
        - Strategic controlling entity (e.g. SASAC) is SOE.
        """
        is_soe = ownership_pct > 0.50
        
        strategic_entities = ["SASAC", "TEMASEK", "MUBADALA", "KIC", "PPIB"]
        if controlling_entity.upper() in strategic_entities:
            is_soe = True
            
        if is_soe:
            logger.info(f"INTL_LOG: Classified as SOE (Ownership: {ownership_pct*100:.1f}%, Controller: {controlling_entity})")
        return is_soe

    def get_risk_rating(self, is_soe: bool, country_code: str) -> str:
        # High risk for SOEs in sanctioned regions
        high_risk_regions = ["CN", "RU", "IR", "KP"]
        if is_soe and country_code.upper() in high_risk_regions:
            return "CRITICAL"
        elif is_soe:
            return "HIGH"
        return "LOW"
