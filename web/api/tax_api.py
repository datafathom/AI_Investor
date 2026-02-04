"""
Tax API - FastAPI Router
REST endpoints for TaxBit analysis and tax-loss harvesting.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.taxes.taxbit_service import get_taxbit_client


def get_taxbit_provider(mock: bool = Query(True)):
    return get_taxbit_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tax_api", tags=["Tax"])

@router.get('/tax/harvesting/opportunities')
async def get_opportunities(
    current_user: Dict[str, Any] = Depends(get_current_user),
    client=Depends(get_taxbit_provider)
):
    """
    Get tax loss harvesting opportunities using TaxBit client.
    """
    try:
        portfolio_id = "port_mock_001"
        data = await client.get_harvesting_opportunities(portfolio_id)
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Failed to fetch tax analysis: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
