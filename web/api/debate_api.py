from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from services.agents.debate_orchestrator import DebateOrchestrator

router = APIRouter(prefix="/api/v1/ai/debate", tags=["AI Debate"])

# Request Models
class DebateStartRequest(BaseModel):
    ticker: str
    context: Optional[Dict] = None

class ArgumentInjectRequest(BaseModel):
    argument: str
    sentiment: Optional[str] = "NEUTRAL"

@router.post("/sessions")
@router.post("/start")
async def start_debate(request: DebateStartRequest):
    """Initialize a new debate session."""
    orchestrator = DebateOrchestrator()
    session = orchestrator.start_debate(request.ticker, request.context)
    return session

@router.get("/stream")
async def stream_active_session():
    """Streaming endpoint alias for the active session."""
    orchestrator = DebateOrchestrator()
    session = orchestrator.get_session() # Gets active session
    if not session:
         raise HTTPException(status_code=404, detail="No active session found")
    return session

@router.get("/sessions/{session_id}")
async def get_debate_session(session_id: str):
    """Get full session details."""
    orchestrator = DebateOrchestrator()
    session = orchestrator.get_session(session_id)
    if not session:
        # Fallback to current active if ID doesn't match (for demo simplification)
        session = orchestrator.get_session()
        if not session:
             raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/inject")
async def inject_argument_alias(request: ArgumentInjectRequest):
    """Inject argument into active session."""
    orchestrator = DebateOrchestrator()
    try:
        session = orchestrator.inject_argument("user", request.argument, request.sentiment)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sessions/{session_id}/intervene")
async def inject_argument(session_id: str, request: ArgumentInjectRequest):
    """Inject a user argument."""
    orchestrator = DebateOrchestrator()
    try:
        session = orchestrator.inject_argument("user", request.argument, request.sentiment)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sessions/{session_id}/votes")
async def get_votes(session_id: str):
    """Get current votes."""
    # Mocking voting integration with orchestrator for now
    # In real flow, orchestrator would use ConsensusEngine
    from services.agents.consensus_engine import get_consensus_engine
    engine = get_consensus_engine(session_id)
    
    # Auto-seed some mock votes if empty (for demo)
    if not engine.votes:
         engine.cast_vote("The Bull", "APPROVE", 0.9, "Strong momentum")
         engine.cast_vote("The Bear", "REJECT", 0.8, "Overbought RSI")
         engine.cast_vote("Risk Manager", "ABSTAIN", 0.5, "Awaiting more data")

    return engine.calculate_results()

@router.post("/sessions/{session_id}/voting/override")
async def human_override(session_id: str, decision: str):
    from services.agents.consensus_engine import get_consensus_engine
    engine = get_consensus_engine(session_id)
    engine.set_human_override(decision, "Manual User Override")
    return engine.calculate_results()

# -------------------------------------------------------------------------
# History Endpoints (Phase 10)
# -------------------------------------------------------------------------
from services.debate.history_service import history_service

@router.get("/history")
async def list_past_debates(ticker: Optional[str] = None, outcome: Optional[str] = None):
    return await history_service.list_history(ticker, outcome)

@router.get("/history/{session_id}/transcript")
async def get_transcript(session_id: str):
    result = await history_service.get_transcript(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Debate not found")
    return result
