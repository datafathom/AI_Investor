"""
Access Firewall for Asset Protection Trusts
PURPOSE: Block unauthorized external access to protected assets.
         Only the Independent Trustee can authorize access to DAPT assets.
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)


class AccessRequestType(Enum):
    """Types of access requests that may be blocked."""
    COURT_ORDER = "court_order"
    CREDITOR_CLAIM = "creditor_claim"
    IRS_LEVY = "irs_levy"
    DIVORCE_DISCOVERY = "divorce_discovery"
    BANKRUPTCY_TRUSTEE = "bankruptcy_trustee"


class AccessFirewall:
    """
    Prevents unauthorized asset freezing or querying by external parties.
    Only the Independent Trustee can authorize access to APT metadata.
    
    Enhanced with jurisdiction awareness and audit logging.
    """
    
    PROTECTED_JURISDICTIONS = ["Nevada", "Delaware", "South Dakota", "Alaska", "Wyoming"]
    
    def validate_access(self, requester_id: str, action: str, trustee_authorized: bool) -> Dict[str, Any]:
        """
        Validates if an access request should be blocked (original simple method).
        """
        logger.info(f"APT Firewall: Request by {requester_id} to {action}. TrusteeAuth={trustee_authorized}")
        
        if not trustee_authorized:
            logger.warning(f"ACCESS BLOCKED: Potential plaintiff/creditor {requester_id} attempting {action}")
            return {
                "decision": "BLOCK",
                "reason": "Independent Trustee authorization required for APT disclosure.",
                "event": "SECURITY_FIREWALL_TRIGGERED"
            }
            
        return {
            "decision": "ALLOW",
            "reason": "Authorized by Independent Trustee."
        }

    async def process_access_request(
        self,
        trust_id: str,
        request_type: str,
        requestor_name: str,
        requestor_authority: str,
        requested_assets: List[str]
    ) -> Dict[str, Any]:
        """
        Process a formal external access request with full audit trail.
        """
        request_id = str(uuid.uuid4())
        
        # Check trust jurisdiction
        jurisdiction = await self._get_trust_jurisdiction(trust_id)
        
        # Determine decision based on jurisdiction protection
        if jurisdiction in self.PROTECTED_JURISDICTIONS:
            decision = "BLOCKED"
            reason = f"Trust protected under {jurisdiction} law. Trustee authorization required."
        elif request_type == AccessRequestType.IRS_LEVY.value:
            decision = "ESCALATED"
            reason = "IRS levy escalated to legal counsel for review."
        else:
            decision = "PENDING_TRUSTEE"
            reason = "Request pending Independent Trustee review."
        
        # Log the access attempt
        await self._log_access_attempt(request_id, trust_id, request_type, requestor_name, decision, reason)
        
        logger.warning(f"Access Firewall: {request_type} from {requestor_name} -> {decision}")
        
        return {
            "request_id": request_id,
            "trust_id": trust_id,
            "request_type": request_type,
            "requestor": requestor_name,
            "authority": requestor_authority,
            "assets_requested": requested_assets,
            "decision": decision,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _get_trust_jurisdiction(self, trust_id: str) -> str:
        """Get the legal jurisdiction of a trust."""
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    SELECT jurisdiction FROM trust_stipulations
                    WHERE trust_id = %s LIMIT 1
                """, (uuid.UUID(trust_id),))
                row = cur.fetchone()
                return row[0] if row else "Unknown"
        except Exception as e:
            logger.error(f"Error getting jurisdiction: {e}")
            return "Unknown"
    
    async def _log_access_attempt(
        self,
        request_id: str,
        trust_id: str,
        request_type: str,
        requestor: str,
        decision: str,
        reason: str
    ) -> None:
        """Log access attempt to audit trail."""
        try:
            with db_manager.pg_cursor() as cur:
                details = f'{{"request_id": "{request_id}", "trust_id": "{trust_id}", "type": "{request_type}", "requestor": "{requestor}", "decision": "{decision}"}}'
                cur.execute("""
                    INSERT INTO activity_logs (user_id, activity_type, details)
                    VALUES ('SYSTEM', 'ACCESS_FIREWALL', %s)
                """, (details,))
        except Exception as e:
            logger.error(f"Error logging access attempt: {e}")


# Singleton
_instance: Optional[AccessFirewall] = None

def get_access_firewall() -> AccessFirewall:
    global _instance
    if _instance is None:
        _instance = AccessFirewall()
    return _instance

