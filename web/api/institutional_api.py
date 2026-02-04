"""
==============================================================================
FILE: web/api/institutional_api.py
ROLE: Institutional API Endpoints (FastAPI)
PURPOSE: REST endpoints for institutional features and professional tools.
==============================================================================
"""

from fastapi import APIRouter, Depends, Query, HTTPException, Request, Response
from typing import Dict, List, Optional
import logging
from web.auth_utils import get_current_user
from services.institutional.institutional_service import get_institutional_service
from services.institutional.professional_tools_service import get_professional_tools_service
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/institutional", tags=["institutional"])

class ClientCreateRequest(BaseModel):
    advisor_id: str
    client_name: str
    jurisdiction: str = "US"
    funding_source: Optional[str] = None
    strategy: str = "Aggressive AI"

class WhiteLabelConfigRequest(BaseModel):
    organization_id: str
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    custom_domain: Optional[str] = None
    branding_name: Optional[str] = None

class ReportGenerateRequest(BaseModel):
    advisor_id: str
    client_id: str
    report_type: str
    content: Dict = {}


@router.post("/client/create")
async def create_client(
    payload: ClientCreateRequest,
    service = Depends(get_institutional_service)
):
    """
    Create client for advisor.
    """
    try:
        client = await service.create_client(
            advisor_id=payload.advisor_id, 
            client_name=payload.client_name,
            jurisdiction=payload.jurisdiction,
            funding_source=payload.funding_source,
            strategy=payload.strategy
        )
        
        return {
            'success': True,
            'data': client.model_dump()
        }
        
    except Exception as e:
        logger.exception(f"Error creating client: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.post("/whitelabel/configure")
async def configure_white_label(payload: WhiteLabelConfigRequest):
    """
    Configure white-label branding.
    """
    try:
        service = get_institutional_service()
        config = await service.configure_white_label(
            organization_id=payload.organization_id,
            logo_url=payload.logo_url,
            primary_color=payload.primary_color,
            secondary_color=payload.secondary_color,
            custom_domain=payload.custom_domain,
            branding_name=payload.branding_name
        )
        
        return {
            'success': True,
            'data': config.model_dump()
        }
        
    except Exception as e:
        logger.exception(f"Error configuring white-label: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clients")
async def get_clients(current_user: dict = Depends(get_current_user)):
    """Get all clients for the logged-in advisor."""
    try:
        advisor_id = current_user.get('user_id')
        service = get_institutional_service()
        clients = await service.get_clients_for_advisor(advisor_id)
        
        return {
            'success': True,
            'data': [c.model_dump() for c in clients]
        }
    except Exception as e:
        logger.exception(f"Error fetching clients for advisor {current_user.get('user_id')}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/fees")
async def get_fee_analytics(
    client_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get fee analytics for an advisor or specific client."""
    try:
        service = get_institutional_service()
        data = await service.get_revenue_forecast(client_id)
        
        return {
            'success': True,
            'data': data
        }
    except Exception as e:
        logger.exception(f"Error fetching fee analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/risk/{client_id}")
async def get_risk_analytics(
    client_id: str,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_institutional_service)
):
    """Get risk analytics for a specific client."""
    try:
        data = await service.get_client_risk_profile(client_id)
        
        return {
            'success': True,
            'data': data
        }
    except Exception as e:
        logger.exception(f"Error fetching risk analytics for client {client_id}: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get("/analytics/signatures/{client_id}")
async def get_signatures(
    client_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get signature status for a specific client."""
    try:
        service = get_institutional_service()
        data = await service.get_signature_status(client_id)
        
        return {
            'success': True,
            'data': data
        }
    except Exception as e:
        logger.exception(f"Error fetching signatures for client {client_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/allocation/{client_id}")
async def get_allocation(
    client_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get asset allocation for a specific client."""
    try:
        service = get_institutional_service()
        data = await service.get_asset_allocation(client_id)
        
        return {
            'success': True,
            'data': data
        }
    except Exception as e:
        logger.exception(f"Error fetching allocation for client {client_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/rebalance/{client_id}")
async def calculate_drift_and_rebalance(
    client_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Calculate portfolio drift and trigger auto-rebalance for a client.
    """
    try:
        service = get_institutional_service()
        allocation_data = await service.get_asset_allocation(client_id)
        
        # Calculate total drift
        total_drift = sum(
            abs(alloc.get('drift', 0)) 
            for alloc in allocation_data.get('allocations', [])
        )
        
        # Simulate rebalance actions
        actions = []
        for alloc in allocation_data.get('allocations', []):
            drift = alloc.get('drift', 0)
            if abs(drift) > 1:  # Only act on significant drift
                action = 'BUY' if drift < 0 else 'SELL'
                actions.append({
                    'category': alloc.get('category'),
                    'action': action,
                    'adjustment_pct': abs(drift)
                })
        
        return {
            'success': True,
            'data': {
                'client_id': client_id,
                'drift_percentage': total_drift,
                'actions': actions,
                'rebalanced': len(actions) > 0,
                'message': f'Rebalanced {len(actions)} positions' if actions else 'No rebalancing needed'
            }
        }
    except Exception as e:
        logger.exception(f"Error calculating drift for client {client_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/report/generate")
async def generate_professional_report(
    payload: ReportGenerateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate professional report.
    """
    try:
        service = get_professional_tools_service()
        report = await service.generate_professional_report(
            advisor_id=payload.advisor_id,
            client_id=payload.client_id,
            report_type=payload.report_type,
            content=payload.content
        )
        
        return {
            'success': True,
            'data': report.model_dump()
        }
        
    except Exception as e:
        logger.exception(f"Error generating professional report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
