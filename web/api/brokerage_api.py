from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from services.brokerage.brokerage_service import get_brokerage_service
import logging
import asyncio

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
        data = await asyncio.to_thread(service.get_status)
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting brokerage status: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/providers')
async def get_supported_providers(service = Depends(get_brokerage_service)):
    """Returns the list of supported brokerage/vendor integrations."""
    try:
        data = await asyncio.to_thread(service.get_supported_providers)
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting providers: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/positions')
async def get_brokerage_positions(service = Depends(get_brokerage_service)):
    """Fetches all open positions from the connected broker."""
    try:
        data = await asyncio.to_thread(service.get_positions)
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
@router.get('/accounts')
async def get_all_accounts():
    """Aggregated accounts view."""
    return {"success": True, "data": [
        {"broker": "IBKR", "id": "U123456", "type": "MARGIN", "buying_power": 50000.0, "nav": 105000.0},
        {"broker": "Robinhood", "id": "RH98765", "type": "CASH", "buying_power": 1200.0, "nav": 5500.0},
        {"broker": "Schwab", "id": "SCH5555", "type": "IRA", "buying_power": 0.0, "nav": 250000.0}
    ]}

@router.get('/balances')
async def get_total_balance():
    """Total aggregated balance."""
    return {"success": True, "data": {
        "total_nav": 360500.0,
        "day_change": 1250.50,
        "day_change_pct": 0.35,
        "cash_balance": 15000.0,
        "margin_used": 5000.0
    }}

@router.post('/sync')
async def sync_transactions():
    """Trigger transaction sync."""
    return {"success": True, "data": {"status": "SYNCING", "job_id": "job_sync_001"}}


@router.get('/connections')
async def list_connections():
    """List active broker connections."""
    return {"success": True, "data": [
        {"id": "conn_ibkr_01", "broker": "IBKR", "status": "CONNECTED", "last_sync": "2 mins ago"},
        {"id": "conn_schwab_02", "broker": "Schwab", "status": "CONNECTED", "last_sync": "5 mins ago"},
        {"id": "conn_rh_03", "broker": "Robinhood", "status": "DISCONNECTED", "last_sync": "1 day ago"}
    ]}


@router.post('/connections')
async def create_connection(data: ConnectRequest):
    """Add a new broker connection."""
    return {"success": True, "data": {"id": "conn_new_01", "status": "PENDING_OAUTH"}}
