"""
==============================================================================
FILE: web/api/ethereum_api.py
ROLE: Ethereum API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for Ethereum wallet balance and token queries.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Path, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.crypto.ethereum_client import get_eth_client as _get_eth_client

def get_eth_client_provider():
    return _get_eth_client()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ethereum", tags=["Ethereum"])


class ValidateAddressRequest(BaseModel):
    address: str


@router.get("/balance/{address}")
async def get_balance(
    address: str = Path(...),
    client = Depends(get_eth_client_provider)
):
    """Get ETH balance for an address."""
    try:
        balance = await client.get_eth_balance(address)
        
        return {
            "success": True,
            "data": {
                "address": address,
                "balance_eth": balance,
                "balance_wei": int(balance * 1e18) if balance else 0
            }
        }
    except Exception as e:
        logger.exception("Failed to get ETH balance")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/tokens/{address}")
async def get_tokens(
    address: str = Path(...),
    client = Depends(get_eth_client_provider)
):
    """Get all ERC-20 token balances for an address."""
    try:
        tokens = await client.get_all_token_balances(address)
        
        return {
            "success": True,
            "data": {
                "address": address,
                "tokens": tokens,
                "count": len(tokens)
            }
        }
    except Exception as e:
        logger.exception("Failed to get token balances")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/gas-price")
async def get_gas_price(client = Depends(get_eth_client_provider)):
    """Get current gas price estimate."""
    try:
        gas_price = await client.get_gas_price()
        
        return {
            "success": True,
            "data": {
                "gas_price_gwei": gas_price,
                "gas_price_wei": gas_price * 1e9
            }
        }
    except Exception as e:
        logger.exception("Failed to get gas price")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/validate-address")
async def validate_address(
    request: ValidateAddressRequest,
    client = Depends(get_eth_client_provider)
):
    """Validate Ethereum address format."""
    try:
        is_valid = client.validate_address(request.address)
        
        return {
            "success": True,
            "data": {
                "address": request.address,
                "valid": is_valid
            }
        }
    except Exception as e:
        logger.exception("Address validation failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
