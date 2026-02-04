"""
==============================================================================
FILE: web/api/privacy_api.py
ROLE: Privacy Endpoints (FastAPI)
PURPOSE: GDPR data export and account deletion endpoints.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from services.system.privacy_service import get_privacy_service
from web.auth_utils import get_current_user


def get_privacy_provider():
    return get_privacy_service()
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/privacy", tags=["Privacy"])


@router.get("/export")
async def export_data(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_privacy_provider)
):
    """
    Trigger a GDPR data export for the authenticated user.
    """
    user_id = current_user.get("id") or current_user.get("user_id")
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Unauthorized"})
    try:
        data = service.export_user_data(user_id)
        return Response(
            content=json.dumps({"success": True, "data": data}, indent=2),
            media_type='application/json',
            headers={'Content-Disposition': 'attachment;filename=my_data.json'}
        )
    except Exception as e:
        logger.exception("Failed to export user data")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.delete("/forget-me")
async def delete_account(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_privacy_provider)
):
    """
    Trigger the 'Right to be Forgotten' for the authenticated user.
    """
    user_id = current_user.get("id") or current_user.get("user_id")
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Unauthorized"})

    success = service.delete_user_account(user_id)
    if success:
        return {"success": True, "data": {"message": "Account and data deleted successfully"}}
    return JSONResponse(status_code=500, content={"success": False, "detail": "Failed to delete account"})
