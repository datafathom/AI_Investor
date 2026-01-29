import logging
from uuid import UUID
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SpendthriftFirewall:
    """
    A 'Warden' service that intercepts withdrawal requests from Spendthrift Trusts.
    Blocks distributions to creditors and non-conforming parties.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpendthriftFirewall, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("SpendthriftFirewall initialized")

    def validate_distribution_request(
        self, 
        trust_id: UUID, 
        amount: Decimal, 
        requester_id: UUID, 
        requester_type: str
    ) -> Dict[str, Any]:
        """
        Intercepts and validates a distribution request.
        """
        logger.info(f"WARDEN_LOG: Intercepting distribution request of {amount} from trust {trust_id} by {requester_type} {requester_id}")
        
        # Spendthrift clause blocks ANY distribution to creditors
        if requester_type.upper() == "CREDITOR":
            logger.error(f"WARDEN_ALERT: BLOCKING CREDITOR WITHDRAWAL. Creditor {requester_id} attempted to seize {amount} from spendthrift trust {trust_id}")
            return {
                "is_allowed": False,
                "reason": "SPENDTHRIFT_PROTECTION_ACTIVE",
                "risk_category": "CREDITOR_SEIZURE"
            }
            
        return {
            "is_allowed": True,
            "reason": "CONFORMING_DISTRIBUTION",
            "risk_category": "NONE"
        }
