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

    async def get_connectors(self) -> List[APIConnector]:
        return self._connectors

    async def test_connector(self, connector_id: str) -> Dict:
        logger.info(f"Testing connector {connector_id}")
        return {"status": "success", "latency": "145ms"}

    async def get_api_keys(self) -> List[APIKey]:
        return self._keys

    async def create_api_key(self, label: str) -> Dict:
        new_id = str(uuid.uuid4())
        key = f"ak_live_{uuid.uuid4().hex}"
        self._keys.append(APIKey(new_id, label, key[:8] + "...", datetime.now().strftime("%Y-%m-%d")))
        return {"id": new_id, "key": key}

    async def get_webhooks(self) -> List[Webhook]:
        return self._webhooks

    async def add_webhook(self, url: str, events: List[str]) -> Webhook:
        wh = Webhook(str(uuid.uuid4()), url, events, "active")
        self._webhooks.append(wh)
        return wh
        
    async def test_webhook(self, webhook_id: str) -> Dict:
        logger.info(f"Testing webhook {webhook_id}")
        return {"status": "success", "delivery_rate": "100%"}

    async def get_available_integrations(self) -> List[Dict]:
        return [
            {"id": "int_1", "name": "Salesforce", "category": "CRM", "description": "Sync customer data", "icon": "cloud"},
            {"id": "int_2", "name": "Slack", "category": "Communication", "description": "Send alerts to channels", "icon": "message-circle"},
            {"id": "int_3", "name": "QuickBooks", "category": "Finance", "description": "Sync invoices and expenses", "icon": "dollar-sign"},
            {"id": "int_4", "name": "Jira", "category": "Project Mgmt", "description": "Create tickets from alerts", "icon": "trello"},
             {"id": "int_5", "name": "Google Sheets", "category": "Data", "description": "Export reports to sheets", "icon": "table"},
        ]

    async def get_connected_integrations(self, user_id: str) -> List[Dict]:
        return [
            {"id": "conn_101", "integration_id": "int_2", "name": "Slack", "status": "active", "connected_at": "2024-01-15T10:00:00"},
            {"id": "conn_102", "integration_id": "int_5", "name": "Google Sheets", "status": "active", "connected_at": "2024-02-01T14:30:00"},
        ]

    async def get_sync_history(self, user_id: str, limit: int) -> List[Dict]:
        return [
            {"id": "sync_501", "connector": "Salesforce", "status": "success", "records": 150, "timestamp": "2024-02-09T08:00:00"},
             {"id": "sync_500", "connector": "QuickBooks", "status": "failed", "error": "Auth token expired", "timestamp": "2024-02-08T18:00:00"},
             {"id": "sync_499", "connector": "Slack", "status": "success", "records": 1, "timestamp": "2024-02-08T12:00:00"},
        ]

# Singleton
_integrations_service: Optional[IntegrationsService] = None

def get_integrations_service() -> IntegrationsService:
    global _integrations_service
    if _integrations_service is None:
        _integrations_service = IntegrationsService()
    return _integrations_service
