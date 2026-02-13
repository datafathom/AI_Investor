from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from typing import List, Dict
from services.ingestion.webhook_service import WebhookService, WebhookEvent

router = APIRouter(prefix="/api/v1/webhooks", tags=["Webhooks"])

@router.post("/receiver/{source}")
async def receive_webhook(source: str, request: Request):
    service = WebhookService()
    try:
        payload = await request.json()
    except Exception:
        payload = {"raw_body": (await request.body()).decode("utf-8")}
    
    headers = dict(request.headers)
    event_id = await service.receive_webhook(source, payload, headers)
    return {"success": True, "event_id": event_id}

@router.get("/events", response_model=List[WebhookEvent])
async def list_events(limit: int = 50):
    service = WebhookService()
    return await service.get_recent_events(limit)

@router.get("/events/{id}", response_model=WebhookEvent)
async def get_event_details(id: str):
    service = WebhookService()
    event = await service.get_event(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
