import logging
from uuid import UUID
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ClawbackPreventer:
    """
    Warden logic to prevent illegal 'clawbacks' from Irrevocable Trusts.
    Taking assets back into the grantor's name invalidates estate tax exclusion.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClawbackPreventer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("ClawbackPreventer initialized")

    def validate_withdrawal(self, trust_id: UUID, trust_type: str, amount: Decimal, recipient_id: UUID, grantor_id: UUID) -> Dict[str, Any]:
        """
        Validates a withdrawal request to ensure it is not an illegal clawback.
        """
        is_irrevocable = trust_type.upper() == "IRREVOCABLE"
        is_grantor_recipient = recipient_id == grantor_id
        
        # Illegal if Irrevocable AND recipient is the grantor
        is_illegal_clawback = is_irrevocable and is_grantor_recipient
        
        if is_illegal_clawback:
            logger.error(f"WARDEN_ALERT: BLOCKING ILLEGAL CLAWBACK. Grantor {grantor_id} attempted withdrawal of {amount} from IRREVOCABLE trust {trust_id}")
            return {
                "is_valid": False,
                "reason": "ILLEGAL_CLAWBACK_IN_IRREVOCABLE_TRUST",
                "risk_level": "CRITICAL"
            }
            
        return {
            "is_valid": True,
            "reason": "DISTRIBUTION_VALID",
            "risk_level": "LOW"
        }
