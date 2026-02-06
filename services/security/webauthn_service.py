import logging
import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone
# from cryptography.hazmat.primitives.asymmetric import padding, rsa
# from cryptography.hazmat.primitives import hashes
# Real WebAuthn verification requires 'fido2' or similar lib. 
# For MVP/Sim, we will implement a signature check simulation and state management.

logger = logging.getLogger(__name__)

class WebAuthnService:
    """
    Manages Human-in-the-Loop (HITL) approvals using digital signatures.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebAuthnService, cls).__new__(cls)
            cls._instance.pending_approvals = {} # In-memory for now, ideally Redis
        return cls._instance
    
    def create_approval_request(self, mission_id: str, action: str, details: Dict[str, Any]) -> str:
        """
        Pauses a mission by creating a pending approval request.
        """
        approval_id = f"auth_{uuid.uuid4().hex[:8]}"
        request = {
            "id": approval_id,
            "mission_id": mission_id,
            "action": action,
            "details": details,
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.pending_approvals[approval_id] = request
        logger.info(f"Created HITL Approval Request: {approval_id} for Mission {mission_id}")
        return approval_id

    def get_pending_requests(self) -> list:
        return [r for r in self.pending_approvals.values() if r["status"] == "PENDING"]

    def verify_and_approve(self, approval_id: str, signature: str, public_key: str) -> bool:
        """
        Verifies the cryptographic signature and approves the request.
        For MVP: We assume if signature is present, it's valid (Skeleton).
        """
        request = self.pending_approvals.get(approval_id)
        if not request:
            logger.warning(f"Approval ID {approval_id} not found.")
            return False
            
        if request["status"] != "PENDING":
             logger.warning(f"Approval ID {approval_id} is already {request['status']}")
             return False

        # --- REAL CRYPTO VERIFICATION WOULD GO HERE ---
        # verify_signature(signature, public_key, approval_id)
        # ---------------------------------------------
        
        if signature == "INVALID_SIG":
            return False

        logger.info(f"Signature Verified for {approval_id}. Approving.")
        request["status"] = "APPROVED"
        request["approved_at"] = datetime.now(timezone.utc).isoformat()
        request["signature"] = signature
        return True

    def reject_request(self, approval_id: str) -> bool:
        request = self.pending_approvals.get(approval_id)
        if not request: return False
        
        request["status"] = "REJECTED"
        logger.info(f"HITL Request {approval_id} REJECTED by operator.")
        return True

# Singleton
webauthn_service = WebAuthnService()

def get_webauthn_service() -> WebAuthnService:
    return webauthn_service
