"""
==============================================================================
FILE: web/api/coinbase_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Coinbase wallet capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
import logging

from services.payments.coinbase_service import get_coinbase_client as _get_coinbase_client

def get_coinbase_service(mock: bool = True):
    """Dependency for getting the Coinbase service."""
    return _get_coinbase_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/coinbase", tags=["Coinbase"])


@router.post("/wallet/coinbase/connect")
async def connect_wallet(
    mock: bool = Query(True, description="Use mock mode"),
    service = Depends(get_coinbase_service)
):
    """Connect Coinbase Wallet (Mock)."""
    user_id = "user_mock_123"
    
    try:
        result = await service.connect_wallet(user_id)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to connect wallet")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/wallet/coinbase/balance")
async def get_balance(
    mock: bool = Query(True, description="Use mock mode"),
    service = Depends(get_coinbase_service)
):
    """Get wallet balance."""
    try:
        result = await service.get_wallet_balance()
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to fetch balance")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/wallet/coinbase/transactions")
async def get_transactions(
    mock: bool = Query(True, description="Use mock mode"),
    service = Depends(get_coinbase_service)
):
    """Get wallet transactions."""
    try:
        result = await service.get_transactions()
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to fetch transactions")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
