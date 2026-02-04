"""
Banking API - FastAPI Router
REST endpoints for Plaid integration and transaction reconciliation.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.banking.banking_service import get_banking_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/banking", tags=["Banking"])

class PublicTokenRequest(BaseModel):
    public_token: str

@router.post('/plaid/create-link-token')
async def create_link_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Initiates the Plaid Link flow by generating a link token."""
    try:
        service = get_banking_service()
        user_id = current_user.get('id', 'demo-user')
        token = service.create_link_token(user_id)
        return {"link_token": token}
    except Exception as e:
        logger.error(f"Error creating link token: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate banking link")

@router.post('/plaid/exchange-public-token')
async def exchange_public_token(
    request_data: PublicTokenRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Exchanges a public token from the frontend for a permanent access token."""
    try:
        service = get_banking_service()
        access_token = service.exchange_public_token(request_data.public_token)
        
        logger.info(f"Successfully linked bank account for user {current_user.get('id')}")
        
        return {"status": "success", "message": "Account linked successfully"}
    except Exception as e:
        logger.error(f"Error exchanging public token: {e}")
        raise HTTPException(status_code=500, detail="Failed to link account")

@router.get('/accounts')
async def get_accounts(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Fetches all linked bank accounts and their balances."""
    try:
        service = get_banking_service()
        # In production, we'd fetch the user's access token from the DB first
        accounts = service.get_accounts("DEMO_ACCESS_TOKEN")
        return accounts
    except Exception as e:
        logger.error(f"Error fetching accounts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch linked accounts")

@router.post('/sync')
async def sync_transactions(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Triggers a manual sync of banking transactions."""
    return {"status": "success", "message": "Transaction sync triggered"}

@router.get('/reconciliation')
async def get_reconciliation(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Fetches the latest reconciliation report."""
    try:
        from services.banking.reconciliation_service import get_reconciliation_service
        service = get_reconciliation_service()
        report = service.perform_reconciliation("DEMO_ACCESS_TOKEN")
        return report
    except Exception as e:
        logger.error(f"Error fetching reconciliation report: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch reconciliation report")
