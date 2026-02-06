"""
Growth API - Venture & Cap-Table Modeling
Phase 8 Implementation: The Global HQ
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging

from services.growth.venture_service import get_venture_service, ShareClass
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/growth", tags=["Growth"])

class WaterfallRequest(BaseModel):
    exit_value: float
    common_shares: int
    cap_table: List[Dict[str, Any]]

@router.post("/waterfall")
async def calculate_waterfall(
    request: WaterfallRequest,
    service = Depends(get_venture_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Calculate exit proceeds for each share class.
    """
    try:
        # Convert raw dicts to ShareClass objects
        cap_table = [ShareClass(**sc) for sc in request.cap_table]
        result = service.calculate_waterfall(
            request.exit_value, 
            cap_table, 
            request.common_shares
        )
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Waterfall calculation failed")
        return {"success": False, "detail": str(e)}

@router.get("/metrics")
async def get_growth_metrics():
    """
    Placeholder for conglomerate-level growth metrics.
    """
    return {
        "success": True, 
        "data": {
            "total_aum": 12500000.0,
            "venture_exposure": 0.15,
            "active_deals": 3
        }
    }
