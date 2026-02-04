"""
==============================================================================
FILE: web/api/plaid_api.py
ROLE: Plaid API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for Plaid bank account linking and balance checks.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Header, Query, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from services.banking.plaid_service import get_plaid_service


def get_plaid_provider():
    return get_plaid_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/plaid", tags=["Plaid"])


class LinkTokenRequest(BaseModel):
    client_name: str = "AI Investor"


class ExchangeTokenRequest(BaseModel):
    public_token: str


class OverdraftCheckRequest(BaseModel):
    account_id: str
    deposit_amount: float


@router.post("/link-token")
async def create_link_token(
    request: LinkTokenRequest,
    x_user_id: str = Header("demo-user"),
    service=Depends(get_plaid_provider)
):
    """
    Create Plaid Link token for frontend initialization.
    """
    try:
        link_token = await service.create_link_token(
            user_id=x_user_id,
            client_name=request.client_name
        )
        
        return {
            "success": True,
            "data": {
                "link_token": link_token,
                "expiration": None
            }
        }
    except Exception as e:
        logger.exception("Failed to create link token")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.post("/exchange-token")
async def exchange_token(
    payload: ExchangeTokenRequest,
    x_user_id: str = Header("demo-user"),
    service=Depends(get_plaid_provider)
):
    """
    Exchange public token for access token.
    """
    try:
        result = await service.exchange_public_token(
            public_token=payload.public_token,
            user_id=x_user_id
        )
        
        return {
            "success": True,
            "data": {
                "item_id": result.get("item_id"),
                "accounts": result.get("accounts", []),
                "access_token": result.get("access_token")
            }
        }
    except Exception as e:
        logger.exception("Failed to exchange token")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/accounts")
async def get_accounts(
    authorization: str = Header(...),
    service=Depends(get_plaid_provider)
):
    """
    Get linked bank accounts.
    """
    try:
        if not authorization.startswith('Bearer '):
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing or invalid Authorization header"})
        
        access_token = authorization[7:]
        
        accounts = await service.get_accounts(access_token)
        
        return {
            "success": True,
            "data": {
                "accounts": accounts
            }
        }
    except Exception as e:
        logger.exception("Failed to get accounts")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.get("/balance")
async def get_balance(
    authorization: str = Header(...),
    x_user_id: str = Header("demo-user"),
    account_id: Optional[str] = Query(None),
    service=Depends(get_plaid_provider)
):
    """
    Get account balance(s).
    """
    try:
        if not authorization.startswith('Bearer '):
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing or invalid Authorization header"})
        
        access_token = authorization[7:]
        
        balance_data = await service.get_balance(
            access_token=access_token,
            account_id=account_id,
            user_id=x_user_id
        )
        
        return {"success": True, "data": balance_data}
        
    except RuntimeError as e:
        if "rate limit" in str(e).lower():
            return JSONResponse(
                status_code=429,
                content={"success": False, "detail": str(e)}
            )
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
    except Exception as e:
        logger.exception("Failed to get balance")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.post("/check-overdraft")
async def check_overdraft(
    payload: OverdraftCheckRequest,
    authorization: str = Header(...),
    x_user_id: str = Header("demo-user"),
    service=Depends(get_plaid_provider)
):
    """
    Check if account has sufficient balance for deposit.
    """
    try:
        if not authorization.startswith('Bearer '):
            return JSONResponse(status_code=401, content={"success": False, "detail": "Missing or invalid Authorization header"})
        
        access_token = authorization[7:]
        
        result = await service.check_overdraft_protection(
            access_token=access_token,
            account_id=payload.account_id,
            deposit_amount=payload.deposit_amount,
            user_id=x_user_id
        )
        
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.exception("Failed to check overdraft")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )
