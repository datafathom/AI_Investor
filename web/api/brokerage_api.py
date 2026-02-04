from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from services.brokerage.brokerage_service import get_brokerage_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/brokerage", tags=["Brokerage"])

class ConnectRequest(BaseModel):
    api_key: str
    secret_key: str
    base_url: Optional[str] = None

@router.get('/status')
async def get_brokerage_status(service = Depends(get_brokerage_service)):
    """Returns the current connection status and account summary."""
    try:
        data = service.get_status()
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting brokerage status: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/providers')
async def get_supported_providers(service = Depends(get_brokerage_service)):
    """Returns the list of supported brokerage/vendor integrations."""
    try:
        data = service.get_supported_providers()
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting providers: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/positions')
async def get_brokerage_positions(service = Depends(get_brokerage_service)):
    """Fetches all open positions from the connected broker."""
    try:
        data = service.get_positions()
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting brokerage positions: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/connect')
async def connect_brokerage(
    data: ConnectRequest,
    service = Depends(get_brokerage_service)
):
    """Updates/Validates brokerage API credentials."""
    try:
        success = service.connect_with_keys(data.api_key, data.secret_key, data.base_url)
        if success:
            return {"success": True, "data": {"message": "Brokerage connected successfully"}}
        else:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"success": False, "detail": "Invalid credentials or connection failure"})
    except Exception as e:
        logger.error(f"Error connecting to brokerage: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
