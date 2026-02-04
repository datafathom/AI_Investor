"""
Integrations API - API Marketplace & Webhooks
Phase 66: Endpoints for data connectors, API key management, and webhooks.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

from web.auth_utils import get_current_user
from services.trading.integrations_service import (
    IntegrationsService,
    APIConnector,
    APIKey,
    Webhook,
    get_integrations_service
)


def get_integrations_provider():
    return get_integrations_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/integrations", tags=["Integrations"])

class ConnectorResponse(BaseModel):
    id: str
    name: str
    type: str
    status: str
    last_sync: str

class APIKeyResponse(BaseModel):
    id: str
    label: str
    prefix: str
    created_at: str

class WebhookRequest(BaseModel):
    url: str
    events: List[str]

@router.get("/connectors")
async def list_connectors(
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    try:
        connectors = await service.get_connectors()
        data = [ConnectorResponse(
            id=c.id,
            name=c.name,
            type=c.type,
            status=c.status,
            last_sync=c.last_sync
        ).model_dump() for c in connectors]
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Error listing connectors")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/available")
async def list_available_integrations(
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    """List all available integrations in the marketplace."""
    try:
        # Assuming the service has a method for this, otherwise return empty list
        available = await service.get_available_integrations() if hasattr(service, 'get_available_integrations') else []
        return {'success': True, 'data': available}
    except Exception as e:
        logger.exception(f"Error listing available integrations: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/connected")
async def list_connected_integrations(
    user_id: str = Query(...),
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    """List integrations connected by the user."""
    try:
        connected = await service.get_connected_integrations(user_id) if hasattr(service, 'get_connected_integrations') else []
        return {'success': True, 'data': connected}
    except Exception as e:
        logger.exception(f"Error listing connected integrations for {user_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/sync-history")
async def get_sync_history(
    user_id: str = Query(...),
    limit: int = Query(20),
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    """Get synchronization history for the user's integrations."""
    try:
        history = await service.get_sync_history(user_id, limit) if hasattr(service, 'get_sync_history') else []
        return {'success': True, 'data': history}
    except Exception as e:
        logger.exception(f"Error getting sync history for {user_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post("/connectors/{connector_id}/test")
async def test_connector(
    connector_id: str,
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    try:
        result = await service.test_connector(connector_id)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception(f"Error testing connector {connector_id}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/keys")
async def list_keys(
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    try:
        keys = await service.get_api_keys()
        data = [APIKeyResponse(
            id=k.id,
            label=k.label,
            prefix=k.prefix,
            created_at=k.created_at
        ).model_dump() for k in keys]
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Error listing API keys")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post("/keys")
async def create_key(
    label: str,
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    try:
        result = await service.create_api_key(label)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Error creating API key")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/webhooks")
async def list_webhooks(
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    try:
        webhooks = await service.get_webhooks()
        data = [w.model_dump() if hasattr(w, 'model_dump') else w for w in webhooks]
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Error listing webhooks")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post("/webhooks")
async def add_webhook(
    payload: WebhookRequest,
    service: IntegrationsService = Depends(get_integrations_provider),
    current_user: dict = Depends(get_current_user)
):
    try:
        result = await service.add_webhook(payload.url, payload.events)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception("Error adding webhook")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
