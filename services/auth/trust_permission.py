import logging
from uuid import UUID
from typing import Dict, Any
from services.legal.modification_gate import TrustModificationGate

logger = logging.getLogger(__name__)

class TrustPermissionService:
    """
    Service layer for enforcing trust modification permissions.
    Bridges the auth layer with the legal modification gate.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TrustPermissionService, cls).__new__(cls)
        return cls._instance

    def __init__(self, modification_gate: TrustModificationGate = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.gate = modification_gate or TrustModificationGate()
        self._initialized = True
        logger.info("TrustPermissionService initialized")

    def check_permission(self, trust_id: UUID, trust_type: str, action: str, user_id: UUID) -> bool:
        """
        Validates if a user can perform an action on a trust.
        
        Args:
            trust_id: UUID of the trust
            trust_type: 'REVOCABLE' or 'IRREVOCABLE'
            action: The requested action (e.g., 'WITHDRAW', 'AMEND', 'INVEST')
            user_id: UUID of the requesting user
        """
        logger.info(f"AUTH_LOG: Checking {action} permission for user {user_id} on trust {trust_id} ({trust_type})")
        
        result = self.gate.can_perform_action(trust_type, action)
        
        if not result["is_allowed"]:
            logger.warning(f"AUTH_ALERT: Access DENIED for user {user_id} to perform {action} on {trust_type} trust {trust_id}")
            return False
            
        return True
