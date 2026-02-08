"""
==============================================================================
FILE: web/api/compliance_144a_api.py
ROLE: API Endpoints for Rule 144A Compliance
PURPOSE: Exposes endpoints for holding info, lockups, and sale eligibility.
==============================================================================
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.compliance.rule_144a_service import (
    get_rule_144a_service,
    Rule144AService
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/compliance/144a", tags=["Compliance", "144A"])


class SaleCheckRequest(BaseModel):
    ticker: str
    shares: int
    holder_id: str = "default"


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_compliance_dashboard(
    service: Rule144AService = Depends(get_rule_144a_service)
):
    """Get compliance overview dashboard."""
    return service.get_compliance_dashboard()


@router.get("/lockups", response_model=List[Dict[str, Any]])
async def get_lockup_expirations(
    days_ahead: int = 90,
    service: Rule144AService = Depends(get_rule_144a_service)
):
    """Get upcoming lockup expirations."""
    return service.get_lockup_expirations(days_ahead=days_ahead)


@router.get("/holding/{ticker}", response_model=Dict[str, Any])
async def get_holding_info(
    ticker: str,
    holder_id: str = "default",
    service: Rule144AService = Depends(get_rule_144a_service)
):
    """Get 144A holding information for a position."""
    return service.get_holding_info(ticker, holder_id)


@router.post("/check-sale", response_model=Dict[str, Any])
async def check_sale_eligibility(
    request: SaleCheckRequest,
    service: Rule144AService = Depends(get_rule_144a_service)
):
    """Check if a sale is eligible under Rule 144."""
    return service.check_sale_eligibility(
        ticker=request.ticker,
        shares=request.shares,
        holder_id=request.holder_id
    )
