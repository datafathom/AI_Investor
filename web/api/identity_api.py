"""
Identity API - FastAPI Router
REST endpoints for identity profile management and reconciliation.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.system.identity_service import IdentityService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/identity", tags=["Identity"])

# Singleton service instance
_identity_service = IdentityService()

@router.get('/profile')
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get the current reconciled identity profile and trust score."""
    try:
        user_id = current_user.get('id')
        profile = _identity_service.get_identity_profile(user_id)
        return profile
    except Exception as e:
        logger.exception(f"Error fetching identity profile for user {current_user.get('id')}")
        raise HTTPException(status_code=500, detail='Failed to fetch identity profile')

@router.post('/reconcile')
async def trigger_reconcile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Manually trigger an identity reconciliation run."""
    try:
        user_id = current_user.get('id')
        profile = _identity_service.reconcile_identity(user_id)
        return {'message': 'Reconciliation complete', 'data': profile}
    except Exception as e:
        logger.exception(f"Error reconciling identity for user {current_user.get('id')}")
        raise HTTPException(status_code=500, detail='Reconciliation failed')

@router.post('/manual-verify')
async def manual_verify(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Stub for uploading verification documents."""
    return {'message': 'Manual verification submission received (Stub)'}
