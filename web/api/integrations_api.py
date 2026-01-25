"""
Integrations API - API Marketplace & Webhooks
Phase 66: Endpoints for data connectors, API key management, and webhooks.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

from services.trading.integrations_service import (
    IntegrationsService,
    APIConnector,
    APIKey,
    Webhook,
    get_integrations_service
)

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

@router.get("/connectors", response_model=List[ConnectorResponse])
async def list_connectors(
    service: IntegrationsService = Depends(get_integrations_service)
):
    connectors = await service.get_connectors()
    return [ConnectorResponse(
        id=c.id,
        name=c.name,
        type=c.type,
        status=c.status,
        last_sync=c.last_sync
    ) for c in connectors]

@router.post("/connectors/{connector_id}/test")
async def test_connector(
    connector_id: str,
    service: IntegrationsService = Depends(get_integrations_service)
):
    return await service.test_connector(connector_id)

@router.get("/keys", response_model=List[APIKeyResponse])
async def list_keys(
    service: IntegrationsService = Depends(get_integrations_service)
):
    keys = await service.get_api_keys()
    return [APIKeyResponse(
        id=k.id,
        label=k.label,
        prefix=k.prefix,
        created_at=k.created_at
    ) for k in keys]

@router.post("/keys")
async def create_key(
    label: str,
    service: IntegrationsService = Depends(get_integrations_service)
):
    return await service.create_api_key(label)

@router.get("/webhooks", response_model=List[Webhook])
async def list_webhooks(
    service: IntegrationsService = Depends(get_integrations_service)
):
    return await service.get_webhooks()

@router.post("/webhooks")
async def add_webhook(
    request: WebhookRequest,
    service: IntegrationsService = Depends(get_integrations_service)
):
    return await service.add_webhook(request.url, request.events)
