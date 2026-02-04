"""
==============================================================================
FILE: web/api/solana_api.py
ROLE: Solana API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for Solana wallet balance and SPL token queries.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

from services.crypto.solana_client import get_solana_client
from services.crypto.solana_token_registry import get_token_registry


def get_solana_provider():
    return get_solana_client()


def get_token_registry_provider():
    return get_token_registry()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/solana", tags=["Solana"])


@router.get("/balance/{address}")
async def get_balance(address: str, service=Depends(get_solana_provider)):
    """Get SOL balance for an address."""
    try:
        balance = await service.get_sol_balance(address)
        
        return {
            "success": True,
            "data": {
                "address": address,
                "balance_sol": balance,
                "balance_lamports": int(balance * 1e9) if balance else 0
            }
        }
    except Exception as e:
        logger.exception("Failed to get SOL balance")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/tokens/{address}")
async def get_tokens(address: str, service=Depends(get_solana_provider)):
    """Get SPL token balances for an address."""
    try:
        tokens = await service.get_spl_tokens(address)
        
        return {
            "success": True,
            "data": {
                "address": address,
                "tokens": tokens,
                "count": len(tokens)
            }
        }
    except Exception as e:
        logger.exception("Failed to get SPL tokens")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/transactions/{address}")
async def get_transactions(
    address: str, 
    limit: int = Query(50, ge=1, le=100),
    service=Depends(get_solana_provider)
):
    """Get transaction history with parsed instructions."""
    try:
        transactions = await service.get_transaction_history(address, limit=limit)
        
        return {
            "success": True,
            "data": {
                "address": address,
                "transactions": transactions,
                "count": len(transactions)
            }
        }
    except Exception as e:
        logger.exception("Failed to get transactions")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/token-info/{mint}")
async def get_token_info(mint: str, registry=Depends(get_token_registry_provider)):
    """Get token metadata from registry."""
    try:
        token_info = registry.get_token_info(mint)
        
        return {
            "success": True,
            "data": {
                "mint": mint,
                "token_info": token_info
            }
        }
    except Exception as e:
        logger.exception("Failed to get token info")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )
