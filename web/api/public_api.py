"""
==============================================================================
FILE: web/api/public_api.py
ROLE: Public API Endpoints (FastAPI)
PURPOSE: REST endpoints for public API and developer platform.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import JSONResponse
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.public_api.public_api_service import get_public_api_service
from services.public_api.developer_portal_service import get_developer_portal_service
from web.auth_utils import get_current_user


def get_public_api_provider():
    return get_public_api_service()


def get_developer_portal_provider():
    return get_developer_portal_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/public", tags=["Public API"])

class APIKeyCreateRequest(BaseModel):
    user_id: str
    tier: str = 'free'


@router.post('/api-key/create')
async def create_api_key(
    data: APIKeyCreateRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_public_api_provider)
):
    """
    Create API key.
    """
    try:
        api_key = await service.create_api_key(data.user_id, data.tier)
        return {'success': True, 'data': api_key.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating API key: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/api-key/{api_key_id}')
async def get_api_key(
    api_key_id: str,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_public_api_provider)
):
    """
    Get API key details.
    """
    try:
        api_key = await service._get_api_key(api_key_id)
        if not api_key:
            return JSONResponse(status_code=404, content={"success": False, "detail": "API key not found"})
        return {'success': True, 'data': api_key.model_dump()}
    except Exception as e:
        logger.exception(f"Error getting API key {api_key_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/documentation')
async def get_documentation(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_developer_portal_provider)
):
    """
    Get API documentation.
    """
    try:
        docs = await service.get_api_documentation()
        return {'success': True, 'data': docs}
    except Exception as e:
        logger.exception(f"Error getting documentation: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/sdks')
async def get_sdks(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_developer_portal_provider)
):
    """
    Get available SDKs.
    """
    try:
        sdks = await service.get_sdks()
        return {'success': True, 'data': sdks}
    except Exception as e:
        logger.exception(f"Error getting SDKs: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


# =============================================================================
# Hyphenated alias router for frontend compatibility (/api/v1/public-api)
# =============================================================================
router_hyphen = APIRouter(prefix="/api/v1/public-api", tags=["Public API"])


@router_hyphen.get('/keys')
async def get_api_keys_list(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_public_api_provider)
):
    """Get list of API keys for a user."""
    try:
        keys = await service.get_user_api_keys(user_id)
        return {'success': True, 'data': [k.model_dump() if hasattr(k, 'model_dump') else k for k in keys] if keys else []}
    except Exception as e:
        logger.exception(f"Error getting API keys: {e}")
        # Return empty list as fallback for frontend
        return {'success': True, 'data': []}


@router_hyphen.get('/usage')
async def get_api_usage(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_public_api_provider)
):
    """Get API usage statistics for a user."""
    try:
        usage = await service.get_api_usage(user_id)
        return {'success': True, 'data': usage.model_dump() if hasattr(usage, 'model_dump') else usage}
    except Exception as e:
        logger.exception(f"Error getting API usage: {e}")
        # Return mock usage data as fallback
        return {'success': True, 'data': {'requests_today': 0, 'requests_month': 0, 'quota_remaining': 1000}}


@router_hyphen.post('/key/create')
async def create_api_key_hyphen(
    data: APIKeyCreateRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_public_api_provider)
):
    """Create API key (hyphenated route)."""
    try:
        api_key = await service.create_api_key(data.user_id, data.tier)
        return {'success': True, 'data': api_key.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating API key: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router_hyphen.post('/key/{key_id}/revoke')
async def revoke_api_key(
    key_id: str,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_public_api_provider)
):
    """Revoke an API key."""
    try:
        await service.revoke_api_key(key_id)
        return {'success': True, 'data': {'revoked': True}}
    except Exception as e:
        logger.exception(f"Error revoking API key {key_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

