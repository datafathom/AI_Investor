"""
Mobile API - Mobile Security & Haptics
Phase 65: Endpoints for biometric kill switches and trade authorizations.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging

from services.security.mobile_service import (
    MobileService,
    TradeAuthRequest,
    get_mobile_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/mobile", tags=["Mobile"])

class KillSwitchRequest(BaseModel):
    biometric_token: str

class AuthDecisionRequest(BaseModel):
    approve: bool

@router.post("/kill-switch")
async def activate_kill_switch(
    request: KillSwitchRequest,
    service: MobileService = Depends(get_mobile_service)
):
    success = await service.activate_kill_switch(request.biometric_token)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid biometric token")
    return {"status": "success", "message": "Kill switch activated"}

@router.get("/authorize", response_model=List[TradeAuthRequest])
async def list_pending_authorizations(
    service: MobileService = Depends(get_mobile_service)
):
    return await service.get_pending_authorizations()

@router.post("/authorize/{auth_id}")
async def decide_authorization(
    auth_id: str,
    request: AuthDecisionRequest,
    service: MobileService = Depends(get_mobile_service)
):
    success = await service.authorize_trade(auth_id, request.approve)
    if not success:
        raise HTTPException(status_code=404, detail="Authorization request not found")
    return {"status": "success"}
