"""
Debate API - FastAPI Router
Migrated from Flask (web/api/debate_api.py)
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import logging
import asyncio

from agents.debate_chamber_agent import get_debate_agent as _get_debate_agent

def get_debate_provider(mock: bool = True):
    return _get_debate_agent(mock=mock)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai/debate", tags=["AI Debate"])

class DebateStartRequest(BaseModel):
    ticker: str = "SPY"

class ArgumentRequest(BaseModel):
    argument: str

@router.post("/start")
async def start_debate(
    request: DebateStartRequest,
    agent = Depends(get_debate_provider)
):
    """Start a new debate session."""
    ticker = request.ticker.upper()
    
    try:
        result = await agent.conduct_debate(ticker)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception(f"Failed to run debate for {ticker}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/stream")
async def stream_debate(agent = Depends(get_debate_provider)):
    """Get the current state of the debate."""
    
    return {
        "success": True,
        "data": {
            "status": "active",
            "transcript": agent.transcript,
            "consensus": agent.consensus
        }
    }

@router.post("/inject")
async def inject_argument(request: ArgumentRequest):
    """Inject a user argument into the debate."""
    # Mocking successful injection for now
    return {"success": True, "data": {"status": "success", "message": "Argument received"}}

@router.post("/run/{ticker}")
async def run_debate(
    ticker: str,
    agent = Depends(get_debate_provider)
):
    """Trigger a new debate for a ticker."""
    try:
        result = await agent.conduct_debate(ticker)
        return {"success": True, "data": result}
    except Exception as e:
        logger.exception(f"Failed to run debate for {ticker}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
