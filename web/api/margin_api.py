"""
Margin API - Leverage & Liquidation
Phase 64: Endpoints for margin buffers, liquidation distance, and de-leveraging plans.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from services.risk.margin_service import (
    MarginService,
    MarginStatus,
    DeleveragePlan,
    get_margin_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/margin", tags=["Margin"])

class MarginStatusResponse(BaseModel):
    buffer: float
    used: float
    available: float
    liquidation_distance: float
    maintenance_margin: float

class DeleverageRequest(BaseModel):
    target_buffer: float

@router.get("/status", response_model=MarginStatusResponse)
async def get_margin_status(
    portfolio_id: str = "default",
    service: MarginService = Depends(get_margin_service)
):
    status = await service.get_margin_status(portfolio_id)
    return MarginStatusResponse(
        buffer=status.margin_buffer,
        used=status.margin_used,
        available=status.margin_available,
        liquidation_distance=status.liquidation_distance,
        maintenance_margin=status.maintenance_margin
    )

@router.post("/deleverage")
async def generate_deleverage_plan(
    request: DeleverageRequest,
    service: MarginService = Depends(get_margin_service)
):
    plan = await service.generate_deleverage_plan(request.target_buffer)
    return {
        "status": "success",
        "plan": {
            "positions_to_close": plan.positions_to_close,
            "total_to_sell": plan.total_to_sell,
            "new_buffer": plan.new_buffer,
            "urgency": plan.urgency
        }
    }

@router.get("/danger-zone")
async def check_danger_zone(
    portfolio_id: str = "default",
    service: MarginService = Depends(get_margin_service)
):
    is_danger = await service.check_danger_zone(portfolio_id)
    return {"is_danger": is_danger}
