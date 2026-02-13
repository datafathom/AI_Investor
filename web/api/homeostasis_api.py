from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from services.portfolio.homeostasis_service import homeostasis_service
from services.execution.philanthropy_service import philanthropy_service
import logging
import asyncio

logger = logging.getLogger(__name__)


def get_homeostasis_provider():
    return homeostasis_service


def get_philanthropy_provider():
    return philanthropy_service

router = APIRouter(prefix="/api/v1/homeostasis", tags=["Homeostasis"])

class UpdateMetricsRequest(BaseModel):
    net_worth: Optional[float] = None

class DonateRequest(BaseModel):
    amount: float = 0.0

@router.get('/status')
async def get_status(
    homeostasis_service = Depends(get_homeostasis_provider)
):
    try:
        tenant_id = 'default' 
        status = await asyncio.to_thread(homeostasis_service.get_homeostasis_status, tenant_id)
        return {"success": True, "data": status}
    except Exception as e:
        logger.exception("Failed to get homeostasis status")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/update')
async def update_metrics(
    data: UpdateMetricsRequest,
    homeostasis_service = Depends(get_homeostasis_provider)
):
    try:
        tenant_id = 'default' 
        if data.net_worth is not None:
            await asyncio.to_thread(homeostasis_service.update_net_worth, tenant_id, data.net_worth)
            
        status = await asyncio.to_thread(homeostasis_service.get_homeostasis_status, tenant_id)
        return {"success": True, "data": status}
    except Exception as e:
        logger.exception("Failed to update metrics")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/donate')
async def manual_donate(
    data: DonateRequest,
    philanthropy_service = Depends(get_philanthropy_provider)
):
    try:
        tenant_id = 'default' 
        philanthropy_service.donate_excess_alpha(tenant_id, data.amount)
        return {"success": True, "data": {"status": "success", "amount": data.amount}}
    except Exception as e:
        logger.exception("Manual donation failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
