import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PPLIStructureValidator:
    """Validates the legal ownership structure of PPLI policies."""
    
    def validate_ownership(self, owner_type: str, policy_type: str) -> Dict[str, Any]:
        """
        Policy: To be excluded from estate, PPLI must be owned by an Irrevocable Trust (ILIT).
        """
        o_type = owner_type.upper()
        
        is_optimal = (o_type == "IRREVOCABLE_TRUST")
        
        if not is_optimal:
            logger.warning(f"LEGAL_ALERT: PPLI policy owned by {owner_type}. Missing ILIT wrapper; death benefit will be included in taxable estate.")
            
        return {
            "is_estate_tax_shielded": is_optimal,
            "ownership_status": "OPTIMAL_ILIT" if is_optimal else "SUBOPTIMAL_DIRECT",
            "recommendation": "NONE" if is_optimal else "TRANSFER_TO_ILIT"
        }
