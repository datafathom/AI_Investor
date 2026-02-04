"""
==============================================================================
FILE: web/api/payment_transfer_api.py
ROLE: Payment Transfer Endpoints (FastAPI)
PURPOSE: Linked vendor and fund transfer endpoints.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

from web.auth_utils import get_current_user
from services.system.social_auth_service import get_social_auth_service


def get_social_auth_provider():
    return get_social_auth_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/payment_transfer", tags=["Payment Transfer"])


class TransferRequest(BaseModel):
    vendor: str
    amount: float
    direction: str = "deposit"  # deposit or withdraw


@router.get("/linked-vendors")
async def get_linked_vendors(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_auth_provider)
):
    """Returns a list of financial vendors linked to the user's account."""
    user_id = current_user.get("id") or current_user.get("user_id")
    user_email = None
    
    # Extract email from user_id (mock storage lookup)
    for email, udata in service.users.items():
        if str(udata["id"]) == str(user_id):
            user_email = email
            break
            
    if not user_email:
        return JSONResponse(status_code=404, content={"success": False, "detail": "User profile not found"})
        
    vendors = service.get_linked_finance_vendors(user_email)
    return {
        "success": True,
        "data": {
            "user_id": user_id,
            "email": user_email,
            "linked_vendors": vendors
        }
    }


@router.post("/transfer")
async def transfer_funds(
    request: TransferRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_social_auth_provider)
):
    """Initiates a fund transfer from a linked vendor."""
    if not request.vendor or not request.amount:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Vendor and amount are required"})
        
    user_id = current_user.get("id") or current_user.get("user_id")
    user_email = None
    
    for email, udata in service.users.items():
        if str(udata["id"]) == str(user_id):
            user_email = email
            break
            
    if not user_email:
        return JSONResponse(status_code=404, content={"success": False, "detail": "User session invalid"})
        
    result = service.transfer_funds(
        user_email, request.vendor, float(request.amount), request.direction
    )
    
    if result.get("success"):
        return {"success": True, "data": result}
    else:
        return JSONResponse(status_code=400, content={"success": False, "detail": result.get("error", "Transfer failed")})
