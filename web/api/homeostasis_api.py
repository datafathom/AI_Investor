from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from services.portfolio.homeostasis_service import homeostasis_service
from services.execution.philanthropy_service import philanthropy_service

router = APIRouter(prefix="/api/v1/homeostasis", tags=["Homeostasis"])

class UpdateMetricsRequest(BaseModel):
    net_worth: Optional[float] = None

class DonateRequest(BaseModel):
    amount: float = 0.0

@router.get('/status')
async def get_status(request: Request):
    # Mapping Flask g.get to an optional header or query param logic? 
    # For now, keeping the legacy 'default' behavior.
    tenant_id = 'default' 
    status = homeostasis_service.get_homeostasis_status(tenant_id)
    return status

@router.post('/update')
async def update_metrics(data: UpdateMetricsRequest):
    tenant_id = 'default' 
    if data.net_worth is not None:
        homeostasis_service.update_net_worth(tenant_id, data.net_worth)
        
    status = homeostasis_service.get_homeostasis_status(tenant_id)
    return status

@router.post('/donate')
async def manual_donate(data: DonateRequest):
    tenant_id = 'default' 
    philanthropy_service.donate_excess_alpha(tenant_id, data.amount)
    return {"status": "success", "amount": data.amount}
