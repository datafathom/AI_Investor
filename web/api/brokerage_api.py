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
async def get_brokerage_status():
    """Returns the current connection status and account summary."""
    try:
        service = get_brokerage_service()
        return service.get_status()
    except Exception as e:
        logger.error(f"Error getting brokerage status: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch status")

@router.get('/providers')
async def get_supported_providers():
    """Returns the list of supported brokerage/vendor integrations."""
    try:
        service = get_brokerage_service()
        return service.get_supported_providers()
    except Exception as e:
        logger.error(f"Error getting providers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch providers")

@router.get('/positions')
async def get_brokerage_positions():
    """Fetches all open positions from the connected broker."""
    try:
        service = get_brokerage_service()
        return service.get_positions()
    except Exception as e:
        logger.error(f"Error getting brokerage positions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch positions")

@router.post('/connect')
async def connect_brokerage(data: ConnectRequest):
    """Updates/Validates brokerage API credentials."""
    try:
        service = get_brokerage_service()
        success = service.connect_with_keys(data.api_key, data.secret_key, data.base_url)
        if success:
            return {"status": "success", "message": "Brokerage connected successfully"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials or connection failure")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error connecting to brokerage: {e}")
        raise HTTPException(status_code=500, detail=str(e))
