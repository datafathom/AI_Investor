"""
Mobile API - Mobile Security & Haptics
Phase 65: Endpoints for biometric kill switches and trade authorizations.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import logging

from services.security.mobile_service import (
    MobileService,
    TradeAuthRequest,
    get_mobile_service
)


def get_mobile_provider() -> MobileService:
    return get_mobile_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/mobile", tags=["Mobile"])

class KillSwitchRequest(BaseModel):
    biometric_token: str

class AuthDecisionRequest(BaseModel):
    approve: bool

@router.post("/kill-switch")
async def activate_kill_switch(
    request: KillSwitchRequest,
    service: MobileService = Depends(get_mobile_provider)
):
    try:
        success = await service.activate_kill_switch(request.biometric_token)
        if not success:
            return JSONResponse(status_code=401, content={"success": False, "detail": "Invalid biometric token"})
        return {"success": True, "data": {"message": "Kill switch activated"}}
    except Exception as e:
        logger.exception("Error activating kill switch")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/authorize")
async def list_pending_authorizations(
    service: MobileService = Depends(get_mobile_provider)
):
    try:
        auths = await service.get_pending_authorizations()
        return {"success": True, "data": [auth.model_dump() for auth in auths]}
    except Exception as e:
        logger.exception("Error listing authorizations")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post("/authorize/{auth_id}")
async def decide_authorization(
    auth_id: str,
    request: AuthDecisionRequest,
    service: MobileService = Depends(get_mobile_provider)
):
    try:
        success = await service.authorize_trade(auth_id, request.approve)
        if not success:
            return JSONResponse(status_code=404, content={"success": False, "detail": "Authorization request not found"})
        return {"success": True, "data": {"status": "success"}}
    except Exception as e:
        logger.exception("Error deciding authorization")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
