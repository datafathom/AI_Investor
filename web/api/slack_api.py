"""
==============================================================================
FILE: web/api/slack_api.py
ROLE: API Endpoint Layer (FastAPI)
PURPOSE: Exposes Slack messaging capabilities to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

from services.notifications.slack_service import get_slack_client


def get_slack_provider(mock: bool = Query(True)):
    return get_slack_client(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/team/slack", tags=["Slack"])


class SlackMessageRequest(BaseModel):
    channel: str
    text: str


@router.post("/message")
async def post_message(
    request: SlackMessageRequest,
    client=Depends(get_slack_provider)
):
    """
    Post a message to a Slack channel.
    Body: { "channel": "#general", "text": "Hello World" }
    """
    if not request.channel or not request.text:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Missing 'channel' or 'text'"})
    
    try:
        data = await client.post_message(request.channel, request.text)
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to post Slack message")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/channels")
async def get_channels(client=Depends(get_slack_provider)):
    """
    Get list of Slack channels.
    Query: ?mock=true
    """
    try:
        data = await client.get_channels()
        return {"success": True, "data": data}
    except Exception as e:
        logger.exception("Failed to fetch Slack channels")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
