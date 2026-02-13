import logging
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class WebhookEvent(BaseModel):
    id: str
    source: str
    event_type: str
    payload: Dict
    received_at: datetime
    status: str  # "processed", "failed", "ignored"
    processing_log: str = ""

class WebhookService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebhookService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.events: List[WebhookEvent] = []
        self._seed_mock_events()
        self._initialized = True

    def _seed_mock_events(self):
        # Mock incoming data
        self.events.append(WebhookEvent(
            id=str(uuid.uuid4()),
            source="Stripe",
            event_type="payment.succeeded",
            payload={"amount": 5000, "currency": "usd", "customer": "cus_123"},
            received_at=datetime.now(),
            status="processed",
            processing_log="Payment recorded in ledger."
        ))
        self.events.append(WebhookEvent(
            id=str(uuid.uuid4()),
            source="GitHub",
            event_type="push",
            payload={"ref": "refs/heads/main", "commits": [{"id": "abc", "message": "fix bug"}]},
            received_at=datetime.now(),
            status="processed",
            processing_log="Triggered CI pipeline."
        ))
        self.events.append(WebhookEvent(
            id=str(uuid.uuid4()),
            source="Unknown",
            event_type="ping",
            payload={"message": "hello"},
            received_at=datetime.now(),
            status="ignored",
            processing_log="No handler for source 'Unknown'."
        ))

    async def receive_webhook(self, source: str, payload: Dict, headers: Dict) -> str:
        event_id = str(uuid.uuid4())
        event_type = payload.get("type") or headers.get("X-Event-Type") or "unknown"
        
        event = WebhookEvent(
            id=event_id,
            source=source,
            event_type=event_type,
            payload=payload,
            received_at=datetime.now(),
            status="pending"
        )
        self.events.insert(0, event)
        
        # Simulate processing/validation logic
        if source == "Stripe":
             event.status = "processed"
             event.processing_log = "Valid Stripe event."
        else:
             event.status = "processed"
             event.processing_log = "Generic payload stored."

        return event_id

    async def get_recent_events(self, limit: int = 50) -> List[WebhookEvent]:
         return sorted(self.events, key=lambda x: x.received_at, reverse=True)[:limit]

    async def get_event(self, event_id: str) -> Optional[WebhookEvent]:
        return next((e for e in self.events if e.id == event_id), None)
