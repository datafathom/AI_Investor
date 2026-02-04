"""
Assets API - FastAPI Router
REST endpoints for asset management and valuation.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.portfolio.assets_service import assets_service as _assets_service

def get_assets_service():
    """Dependency for getting the assets service."""
    return _assets_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/assets", tags=["Assets"])

class AssetCreateRequest(BaseModel):
    name: str
    value: float
    type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AssetUpdateRequest(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@router.get('/')
async def get_assets(
    service = Depends(get_assets_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all assets."""
    try:
        assets = service.get_all_assets()
        return {"success": True, "data": assets}
    except Exception as e:
        logger.error(f"Error fetching assets: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/', status_code=201)
async def create_asset(
    request_data: AssetCreateRequest,
    service = Depends(get_assets_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new asset."""
    try:
        asset = service.add_asset(request_data.model_dump())
        return {"success": True, "data": asset}
    except Exception as e:
        logger.error(f"Error creating asset: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.put('/{asset_id}')
async def update_asset(
    asset_id: str,
    request_data: AssetUpdateRequest,
    service = Depends(get_assets_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update an existing asset."""
    try:
        updated_asset = service.update_asset(asset_id, request_data.model_dump(exclude_unset=True))
        if updated_asset:
            return {"success": True, "data": updated_asset}
        raise HTTPException(status_code=404, detail='Asset not found')
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating asset: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.delete('/{asset_id}')
async def delete_asset(
    asset_id: str,
    service = Depends(get_assets_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete an asset."""
    try:
        success = service.delete_asset(asset_id)
        if success:
            return {"success": True, "data": {'message': 'Asset deleted'}}
        raise HTTPException(status_code=404, detail='Asset not found')
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting asset: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/valuation')
async def get_valuation(
    service = Depends(get_assets_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get total valuation summary."""
    try:
        total = service.get_total_valuation()
        return {"success": True, "data": {'total_valuation': total, 'currency': 'USD'}}
    except Exception as e:
        logger.error(f"Error getting valuation: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
