from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from agents.debate_chamber_agent import DebateChamberAgentSingleton
import asyncio

router = APIRouter(prefix="/api/v1/ai/debate", tags=["AI Debate"])

# Request Models
class DebateStartRequest(BaseModel):
    ticker: str
    model: Optional[str] = "claude-3-opus"

class ArgumentInjectRequest(BaseModel):
    argument: str

# Singleton access
def get_agent():
    return DebateChamberAgentSingleton.get_instance(mock=True)

async def run_debate_background(ticker: str):
    """Background task to run the debate steps."""
    agent = get_agent()
    # This runs the full cycle which updates agent.transcript internally
    # We can rely on the agent's internal state updates
    await agent.conduct_debate(ticker)

@router.post("/start")
async def start_debate(request: DebateStartRequest, background_tasks: BackgroundTasks):
    """Initialize a new debate session."""
    agent = get_agent()
    
    # Clear previous state
    agent.transcript = []
    agent.consensus = {}
    
    # Start background execution
    background_tasks.add_task(run_debate_background, request.ticker)
    
    return {
        "status": "started",
        "ticker": request.ticker,
        "message": "Debate chamber initialized. Agents entering podium."
    }

@router.get("/stream")
async def stream_debate_state():
    """Poll for the latest transcript and consensus."""
    agent = get_agent()
    return {
        "transcript": agent.transcript,
        "consensus": agent.consensus,
        "active": len(agent.consensus) == 0 # Active if consensus not yet reached
    }

@router.post("/inject")
async def inject_argument(request: ArgumentInjectRequest):
    """Inject a user argument into the active debate."""
    agent = get_agent()
    
    # Create a user entry
    entry = {
        "persona": "User", 
        "reasoning": request.argument,
        "role": "Human Intervener"
    }
    agent.transcript.append(entry)
    
    # Optionally trigger a specific response here? 
    # For now, just appending to log is sufficient for the UI.
    
    return {"status": "injected", "entry": entry}
