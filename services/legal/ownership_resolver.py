import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LegalOwnershipResolver:
    """Resolves the legal and tax ownership of an asset or account."""
    
    def resolve_tax_entity(self, account_type: str, grantor_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Policy:
        - INDIVIDUAL: Person is owner.
        - REVOCABLE_TRUST: Grantor is tax owner (pass-through).
        - IRREVOCABLE_TRUST: Trust is its own tax entity (needs EIN).
        - LLC: Entity is owner (usually pass-through but distinct legal layer).
        """
        acc_type = account_type.upper()
        
        if acc_type == "INDIVIDUAL":
            entity_type = "PERSON"
            is_pass_through = True
        elif acc_type == "REVOCABLE_TRUST":
            entity_type = "PERSON_GRANTOR"
            is_pass_through = True
        elif acc_type == "IRREVOCABLE_TRUST":
            entity_type = "TRUST_ENTITY"
            is_pass_through = False
        elif acc_type == "LLC":
            entity_type = "BUSINESS_ENTITY"
            is_pass_through = True # Defaulting to single-member/pass-through for now
        else:
            entity_type = "UNKNOWN"
            is_pass_through = False
            
        logger.info(f"LEGAL_LOG: Account {account_type} resolved as {entity_type} (Pass-through: {is_pass_through})")
        
        return {
            "entity_type": entity_type,
            "is_pass_through": is_pass_through,
            "requires_separate_tax_filing": not is_pass_through
        }
