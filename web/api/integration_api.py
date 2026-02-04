"""
==============================================================================
FILE: web/api/integration_api.py
ROLE: Integration API Endpoints (FastAPI)
PURPOSE: REST endpoints for third-party app integrations.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from services.integration.integration_framework import get_integration_framework
from services.integration.integration_service import get_integration_service


def get_integration_framework_provider():
    return get_integration_framework()


def get_integration_service_provider():
    return get_integration_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/integration", tags=["Integration"])


class CreateIntegrationRequest(BaseModel):
    user_id: str
    app_name: str
    oauth_token: Optional[str] = None


class SyncIntegrationRequest(BaseModel):
    sync_type: str = 'incremental'


@router.post("/create")
async def create_integration(
    request: CreateIntegrationRequest,
    framework = Depends(get_integration_framework_provider)
):
    """
    Create integration connection.
    """
    try:
        integration = await framework.create_integration(request.user_id, request.app_name, request.oauth_token)
        
        return {
            'success': True,
            'data': integration.model_dump()
        }
    except Exception as e:
        logger.exception("Error creating integration")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/user/{user_id}")
async def get_user_integrations(user_id: str):
    """
    Get integrations for user.
    """
    try:
        # In production, would fetch from database
        return {
            'success': True,
            'data': []
        }
    except Exception as e:
        logger.exception("Error getting integrations")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/{integration_id}/sync")
async def sync_integration(
    integration_id: str,
    payload: SyncIntegrationRequest,
    service = Depends(get_integration_service_provider)
):
    """
    Sync data from integration.
    """
    try:
        job = await service.sync_data(integration_id, payload.sync_type)
        
        return {
            'success': True,
            'data': job.model_dump() if hasattr(job, 'model_dump') else job
        }
    except Exception as e:
        logger.exception("Error syncing integration")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
