"""
==============================================================================
FILE: web/api/coinbase_crypto_api.py
ROLE: Coinbase Crypto API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for Coinbase trading and custody management.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.crypto.coinbase_client import get_coinbase_client as _get_coinbase_client
from services.crypto.coinbase_custody import get_coinbase_custody as _get_coinbase_custody

def get_coinbase_service():
    """Dependency for getting the Coinbase client."""
    return _get_coinbase_client()

def get_coinbase_custody_service():
    """Dependency for getting the Coinbase custody service."""
    return _get_coinbase_custody()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/coinbase_crypto", tags=["Coinbase Crypto"])


class OrderRequest(BaseModel):
    product_id: str
    side: str
    order_configuration: Dict[str, Any]


class WithdrawalRequest(BaseModel):
    vault_id: str
    currency: str
    amount: float
    destination: str


@router.get("/accounts")
async def get_accounts(service = Depends(get_coinbase_service)):
    """Get all trading accounts/balances."""
    try:
        accounts = await service.get_accounts()
        return {"success": True, "data": {"accounts": accounts, "count": len(accounts)}}
    except Exception as e:
        logger.exception("Failed to get accounts")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/trading-pairs")
async def get_trading_pairs(service = Depends(get_coinbase_service)):
    """Get available trading pairs."""
    try:
        pairs = await service.get_trading_pairs()
        return {"success": True, "data": {"trading_pairs": pairs, "count": len(pairs)}}
    except Exception as e:
        logger.exception("Failed to get trading pairs")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/orders")
async def place_order(
    request_data: OrderRequest,
    service = Depends(get_coinbase_service)
):
    """Place a trade order."""
    try:
        result = await service.place_order(
            product_id=request_data.product_id,
            side=request_data.side,
            order_configuration=request_data.order_configuration
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to place order")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/orders")
async def get_orders(
    limit: int = Query(100, ge=1, le=1000),
    service = Depends(get_coinbase_service)
):
    """Get order history."""
    try:
        orders = await service.get_orders(limit=limit)
        return {"success": True, "data": {"orders": orders, "count": len(orders)}}
    except Exception as e:
        logger.exception("Failed to get orders")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/vaults")
async def get_vaults(
    vault_id: Optional[str] = Query(None),
    service = Depends(get_coinbase_custody_service)
):
    """Get vault balances."""
    try:
        balances = await service.get_vault_balances(vault_id=vault_id)
        return {"success": True, "data": {"vault_balances": balances, "count": len(balances)}}
    except Exception as e:
        logger.exception("Failed to get vault balances")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/vaults/withdraw")
async def request_withdrawal(
    request_data: WithdrawalRequest,
    service = Depends(get_coinbase_custody_service)
):
    """Request withdrawal from vault."""
    try:
        result = await service.request_withdrawal(
            vault_id=request_data.vault_id,
            currency=request_data.currency,
            amount=request_data.amount,
            destination=request_data.destination
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Failed to request withdrawal")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
