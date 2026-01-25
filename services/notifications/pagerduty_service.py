"""
==============================================================================
FILE: services/notifications/pagerduty_service.py
ROLE: Incident Management Service
PURPOSE: Interfaces with PagerDuty for triggering and managing critical incidents.
         
INTEGRATION POINTS:
    - IncidentAPI: Primary consumer.
    - SystemHealthService: Future consumer for automated incident triggering.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import uuid
import random
import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class PagerDutyClient:
    """
    Client for PagerDuty API.
    Currently defaults to MOCK MODE as per Phase 22 requirements.
    """
    
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # TODO: Initialize live PagerDuty client here

    async def trigger_incident(self, title: str, urgency: str = "high") -> Dict[str, Any]:
        """
        Trigger a new incident.
        """
        if self.mock:
            await asyncio.sleep(0.6) # Simulate request latency
            
            incident_id = f"P{random.randint(10000, 99999)}"
            logger.info(f"[PagerDuty Mock] Triggered Incident: {title} | Urgency: {urgency}")
            
            return {
                "id": incident_id,
                "title": title,
                "urgency": urgency,
                "status": "triggered",
                "service": {"summary": "AI Investor Backend"},
                "created_at": datetime.datetime.utcnow().isoformat()
            }
        return {}

    async def get_incidents(self) -> List[Dict[str, Any]]:
        """
        Get active incidents.
        """
        if self.mock:
            await asyncio.sleep(0.4)
            # Return some mock active incidents
            return [
                {
                    "id": "P55102",
                    "title": "Database Connection Latency High",
                    "urgency": "high",
                    "status": "acknowledged",
                    "created_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=15)).isoformat()
                },
                {
                    "id": "P55109",
                    "title": "API Rate Limit Warning (AlphaVantage)",
                    "urgency": "low",
                    "status": "triggered",
                    "created_at": (datetime.datetime.utcnow() - datetime.timedelta(minutes=2)).isoformat()
                }
            ]
        return []

_instance = None

def get_pagerduty_client(mock: bool = True) -> PagerDutyClient:
    global _instance
    if _instance is None:
        _instance = PagerDutyClient(mock=mock)
    return _instance
