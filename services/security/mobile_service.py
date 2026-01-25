"""
Mobile Service - Mobile Security & Haptics
Phase 65: Manages biometric kill switches, trade authorization, and mobile alerts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class TradeAuthRequest:
    id: str
    ticker: str
    action: str
    amount: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"

class MobileService:
    def __init__(self) -> None:
        self._kill_switch_active = False
        self._pending_auths: List[TradeAuthRequest] = []
        logger.info("MobileService initialized")

    async def activate_kill_switch(self, biometric_token: str) -> bool:
        # Validate token (mock)
        if biometric_token == "valid_token":
            self._kill_switch_active = True
            logger.critical("MOBILE KILL SWITCH ACTIVATED VIA BIOMETRICS")
            return True
        return False

    async def get_pending_authorizations(self) -> List[TradeAuthRequest]:
        return self._pending_auths

    async def create_auth_request(self, ticker: str, action: str, amount: float) -> str:
        req_id = f"auth-{datetime.now().timestamp()}"
        req = TradeAuthRequest(id=req_id, ticker=ticker, action=action, amount=amount)
        self._pending_auths.append(req)
        # In a real app, this would trigger a PUSH notification
        logger.info(f"Mobile auth requested for {action} {ticker}")
        return req_id

    async def authorize_trade(self, auth_id: str, approve: bool) -> bool:
        for req in self._pending_auths:
            if req.id == auth_id:
                req.status = "approved" if approve else "rejected"
                logger.info(f"Mobile auth {auth_id} result: {req.status}")
                return True
        return False

# Singleton
_mobile_service: Optional[MobileService] = None

def get_mobile_service() -> MobileService:
    global _mobile_service
    if _mobile_service is None:
        _mobile_service = MobileService()
    return _mobile_service
