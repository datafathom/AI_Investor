"""
==============================================================================
FILE: web/api/public_api_endpoints.py
ROLE: Public API Endpoints (FastAPI)
PURPOSE: REST endpoints for public API and developer platform.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging

from services.public_api.public_api_service import get_public_api_service
from services.public_api.developer_portal_service import get_developer_portal_service


def get_public_api_provider():
    return get_public_api_service()


def get_developer_portal_provider():
    return get_developer_portal_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/public", tags=["Public API"])


class CreateAPIKeyRequest(BaseModel):
    user_id: str
    tier: str = 'free'


@router.post("/api-key/create")
async def create_api_key(
    request: CreateAPIKeyRequest,
    service=Depends(get_public_api_provider)
):
    """
    Create API key.
    """
    try:
        api_key = await service.create_api_key(request.user_id, request.tier)
        
        return {
            'success': True,
            'data': api_key.model_dump()
        }
    except Exception as e:
        logger.exception("Error creating API key")
        return JSONResponse(
            status_code=500,
            content={'success': False, 'detail': str(e)}
        )


@router.get("/api-key/{api_key_id}")
async def get_api_key(
    api_key_id: str,
    service=Depends(get_public_api_provider)
):
    """
    Get API key details.
    """
    try:
        api_key = await service._get_api_key(api_key_id)
        
        if not api_key:
            return JSONResponse(
                status_code=404,
                content={'success': False, 'detail': 'API key not found'}
            )
        
        return {
            'success': True,
            'data': api_key.model_dump()
        }
    except Exception as e:
        logger.exception("Error getting API key")
        return JSONResponse(
            status_code=500,
            content={'success': False, 'detail': str(e)}
        )


@router.get("/documentation")
async def get_documentation(service=Depends(get_developer_portal_provider)):
    """
    Get API documentation.
    """
    try:
        docs = await service.get_api_documentation()
        
        return {
            'success': True,
            'data': docs
        }
    except Exception as e:
        logger.exception("Error getting documentation")
        return JSONResponse(
            status_code=500,
            content={'success': False, 'detail': str(e)}
        )


@router.get("/sdks")
async def get_sdks(service=Depends(get_developer_portal_provider)):
    """
    Get available SDKs.
    """
    try:
        sdks = await service.get_sdks()
        
        return {
            'success': True,
            'data': sdks
        }
    except Exception as e:
        logger.exception("Error getting SDKs")
        return JSONResponse(
            status_code=500,
            content={'success': False, 'detail': str(e)}
        )
