"""
Integrations Service - API & Webhooks
Phase 66: Manages external data connectors, API keys, and outbound webhooks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

@dataclass
class APIConnector:
    id: str
    name: str
    type: str  # exchange, news, alternative_data
    status: str
    last_sync: str

@dataclass
class APIKey:
    id: str
    label: str
    prefix: str
    created_at: str

@dataclass
class Webhook:
    id: str
    url: str
    events: List[str]
    status: str

class IntegrationsService:
    def __init__(self) -> None:
        self._connectors = [
            APIConnector("conn-1", "Alpaca Markets", "exchange", "connected", "2026-01-18T23:00:00"),
            APIConnector("conn-2", "Alpha Vantage", "news", "error", "2026-01-18T22:30:00"),
            APIConnector("conn-3", "Polygon.io", "exchange", "connected", "2026-01-18T23:15:00"),
        ]
        self._keys = [
            APIKey("key-1", "Main Dashboard", "ak_live_...", "2026-01-01"),
        ]
        self._webhooks = []
        logger.info("IntegrationsService initialized")

    def get_connectors(self) -> List[APIConnector]:
        return self._connectors

    def test_connector(self, connector_id: str) -> Dict:
        logger.info(f"Testing connector {connector_id}")
        return {"status": "success", "latency": "145ms"}

    def get_api_keys(self) -> List[APIKey]:
        return self._keys

    def create_api_key(self, label: str) -> Dict:
        new_id = str(uuid.uuid4())
        key = f"ak_live_{uuid.uuid4().hex}"
        self._keys.append(APIKey(new_id, label, key[:8] + "...", datetime.now().strftime("%Y-%m-%d")))
        return {"id": new_id, "key": key}

    def get_webhooks(self) -> List[Webhook]:
        return self._webhooks

    def add_webhook(self, url: str, events: List[str]) -> Webhook:
        wh = Webhook(str(uuid.uuid4()), url, events, "active")
        self._webhooks.append(wh)
        return wh
        
    def test_webhook(self, webhook_id: str) -> Dict:
        logger.info(f"Testing webhook {webhook_id}")
        return {"status": "success", "delivery_rate": "100%"}

# Singleton
_integrations_service: Optional[IntegrationsService] = None

def get_integrations_service() -> IntegrationsService:
    global _integrations_service
    if _integrations_service is None:
        _integrations_service = IntegrationsService()
    return _integrations_service
