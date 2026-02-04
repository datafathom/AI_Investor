"""
==============================================================================
FILE: web/api/discord_api.py
ROLE: Discord API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for Discord bot and webhook management.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from services.social.discord_bot import get_discord_bot as _get_discord_bot
from services.communication.discord_webhook import get_discord_webhook as _get_discord_webhook

def get_discord_bot_provider():
    return _get_discord_bot()

def get_discord_webhook_provider(url: str):
    return _get_discord_webhook(url=url)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/discord", tags=["Discord"])


class WebhookTestRequest(BaseModel):
    webhook_url: str


class WebhookAlertRequest(BaseModel):
    webhook_url: str
    title: str
    description: str
    color: int = 0x00ff00


@router.get("/mentions/{ticker}")
async def get_mentions(
    ticker: str = Path(...),
    limit: int = Query(50, ge=1, le=100),
    bot = Depends(get_discord_bot_provider)
):
    """Get Discord mentions for a ticker."""
    try:
        mentions = await bot.get_recent_mentions(ticker, limit=limit)
        
        return {
            "success": True,
            "data": {
                "ticker": ticker,
                "mentions": mentions,
                "count": len(mentions)
            }
        }
    except Exception as e:
        logger.exception("Failed to get mentions")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/hype/{ticker}")
async def get_hype(
    ticker: str = Path(...),
    bot = Depends(get_discord_bot_provider)
):
    """Get hype score for a ticker."""
    try:
        hype = await bot.get_hype_score(ticker)
        return {"success": True, "data": hype}
    except Exception as e:
        logger.exception("Failed to get hype")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/webhook/test")
async def test_webhook(request: WebhookTestRequest):
    """Test webhook configuration (Manual injection for now)."""
    try:
        webhook = _get_discord_webhook(url=request.webhook_url)
        
        success = await webhook.send_alert(
            title="Test Alert",
            description="This is a test alert from AI Investor Terminal",
            color=0x00ff00
        )
        
        return {
            "success": True,
            "data": {
                "success": success,
                "message": "Test alert sent"
            }
        }
    except Exception as e:
        logger.exception("Webhook test failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/webhook/alert")
async def send_alert(request: WebhookAlertRequest):
    """Send alert via webhook (Manual injection for now)."""
    try:
        webhook = _get_discord_webhook(url=request.webhook_url)
        
        success = await webhook.send_alert(request.title, request.description, request.color)
        
        return {
            "success": True,
            "data": {
                "success": success,
                "message": "Alert sent"
            }
        }
    except Exception as e:
        logger.exception("Failed to send alert")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
