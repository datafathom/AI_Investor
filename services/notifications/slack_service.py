"""
==============================================================================
FILE: services/notifications/slack_service.py
ROLE: Team Communication Service
PURPOSE: Interfaces with Slack for broadcasting alerts and reports to team channels.
         
INTEGRATION POINTS:
    - SlackAPI: Primary consumer.
    - AlertManager: Future consumer for routing alerts to specific channels.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SlackClient:
    """
    Client for Slack API.
    Currently defaults to MOCK MODE as per Phase 23 requirements.
    """
    
    def __init__(self, token: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.token = token
        # TODO: Initialize live Slack client here

    async def post_message(self, channel: str, text: str) -> Dict[str, Any]:
        """
        Post a message to a channel.
        """
        if self.mock:
            await asyncio.sleep(0.4) # Simulate network latency
            
            ts = str(datetime.datetime.utcnow().timestamp())
            logger.info(f"[Slack Mock] Posted to {channel}: {text}")
            
            return {
                "ok": True,
                "channel": channel,
                "ts": ts,
                "message": {
                    "text": text,
                    "username": "AI Investor Bot",
                    "bot_id": "B12345678",
                    "type": "message",
                    "subtype": "bot_message",
                    "ts": ts
                }
            }
        return {}

    async def get_channels(self) -> List[Dict[str, Any]]:
        """
        Get list of available channels.
        """
        if self.mock:
            await asyncio.sleep(0.2)
            return [
                {"id": "C01", "name": "general", "num_members": 15},
                {"id": "C02", "name": "random", "num_members": 12},
                {"id": "C03", "name": "alerts-critical", "num_members": 5},
                {"id": "C04", "name": "dev-ops", "num_members": 8},
                {"id": "C05", "name": "market-news", "num_members": 20}
            ]
        return []

_instance = None

def get_slack_client(mock: bool = True) -> SlackClient:
    global _instance
    if _instance is None:
        _instance = SlackClient(mock=mock)
    return _instance
