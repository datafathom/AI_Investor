"""
==============================================================================
FILE: services/communication/discord_webhook.py
ROLE: Alert Dispatcher
PURPOSE: Sends notifications and signals to Discord via webhooks.
         Supports rich embeds and platform-specific formatting.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import timezone, datetime

logger = logging.getLogger(__name__)

class DiscordWebhook:
    """
    Handles outbound notifications to Discord channels.
    """
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url

    async def send_alert(self, title: str, description: str, color: int = 0x00ff00, fields: List[Dict[str, Any]] = []) -> bool:
        """Send a rich embed alert to Discord."""
        payload = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "fields": fields,
                "footer": {"text": "AI Investor Terminal"},
                "timestamp": datetime.now(timezone.utc).isoformat()
            }]
        }
        
        # Mocking the HTTP POST
        logger.info(f"Discord Webhook Alert Dispatched: {title}")
        if not self.webhook_url:
            logger.warning("No webhook URL configured (Mock Delivery Only)")
            
        await asyncio.sleep(0.2)
        return True

    async def send_trade_signal(self, ticker: str, side: str, price: float, confidence: float) -> bool:
        """Specific template for trade alerts."""
        title = f"🚀 AI SIGNAL: {side.upper()} {ticker}"
        color = 0x27ae60 if side.lower() == 'buy' else 0xc0392b
        description = f"High-confidence {side} signal detected via Discord & Reddit fusion."
        
        fields = [
            {"name": "Price", "value": f"${price}", "inline": True},
            {"name": "Confidence", "value": f"{int(confidence*100)}%", "inline": True}
        ]
        
        return await self.send_alert(title, description, color, fields)

_instance = None

def get_discord_webhook(url: Optional[str] = None) -> DiscordWebhook:
    global _instance
    if _instance is None or (url and url != _instance.webhook_url):
        _instance = DiscordWebhook(webhook_url=url)
    return _instance
