from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from services.agent_orchestration_service import get_orchestration_service

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])

# -------------------------------------------------------------------------
# Request Models
# -------------------------------------------------------------------------

class AgentInvokeRequest(BaseModel):
    action: str
    data: Optional[Dict[str, Any]] = {}
    context: Optional[Dict[str, Any]] = None


class AgentDelegateRequest(BaseModel):
    """Request model for agent-to-agent delegation."""
    source_agent: str
    target_agent: str
    sub_task: str
    context: Optional[Dict[str, Any]] = {}

# -------------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------------

@router.get("/")
async def list_agents(dept_id: Optional[int] = None, role: Optional[str] = None):
    """
    List all available agents, optionally filtered by department or role.
    """
    service = get_orchestration_service()
    agents = service.definitions
    
    if dept_id:
        agents = [a for a in agents if a.get("dept_id") == dept_id]
        
    if role:
        agents = [a for a in agents if role.lower() in a.get("role", "").lower()]
        
    return agents

@router.get("/{agent_id}")
async def get_agent_details(agent_id: str):
    """
    Get detailed configuration and status for a specific agent.
    """
    service = get_orchestration_service()
    
    # 1. Check definition
    defn = next((d for d in service.definitions if d["id"] == agent_id), None)
    if not defn:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
        
    # 2. Check runtime status if active
    runtime_agent = service.agents.get(agent_id)
    status = runtime_agent.health_check() if runtime_agent else {"status": "inactive"}
    
    return {
        "definition": defn,
        "runtime_status": status
    }

@router.post("/{agent_id}/invoke")
async def invoke_agent(agent_id: str, request: AgentInvokeRequest):
    """
    Directly invoke an agent by ID.
    """
    service = get_orchestration_service()
    
    # Validate agent availability first
    defn = next((d for d in service.definitions if d["id"] == agent_id), None)
    if not defn:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

    result = await service.invoke_agent(agent_id, request.dict())
    
    if "error" in result:
        # Check for specific error types to set correct HTTP status
        error_msg = result["error"]
        if "System Halted" in error_msg:
            raise HTTPException(status_code=503, detail=result)
        raise HTTPException(status_code=500, detail=result)
        
    return result


@router.post("/delegate")
async def delegate_task(request: AgentDelegateRequest):
    """
    Delegate a sub-task from one agent to another (federation).
    The source agent delegates via request_help() to the target agent.
    """
    service = get_orchestration_service()
    
    # Validate both agents exist
    source_defn = next((d for d in service.definitions if d["id"] == request.source_agent), None)
    target_defn = next((d for d in service.definitions if d["id"] == request.target_agent), None)
    
    if not source_defn:
        raise HTTPException(status_code=404, detail=f"Source agent '{request.source_agent}' not found")
    if not target_defn:
        raise HTTPException(status_code=404, detail=f"Target agent '{request.target_agent}' not found")
    
    # Get or create source agent
    source_agent = service.get_agent(request.source_agent)
    if not source_agent:
        raise HTTPException(status_code=500, detail="Failed to initialize source agent")
    
    # Use federation: source delegates to target
    result = await source_agent.request_help(
        agent_id=request.target_agent,
        sub_task=request.sub_task,
        context=request.context
    )
    
    return {
        "delegation": {
            "source": request.source_agent,
            "target": request.target_agent,
            "sub_task": request.sub_task
        },
        "result": result
    }


# Standardized legacy endpoint for verification scripts
# verify_phase6_perf.py expects /api/v1/ai/agents/invoke with agent_id in payload
legacy_router = APIRouter(prefix="/api/v1/ai/agents", tags=["AI Agents (Legacy)"])

class LegacyInvokeRequest(BaseModel):
    agent_id: str
    payload: Dict[str, Any]

@legacy_router.post("/invoke")
async def legacy_invoke_agent(request: LegacyInvokeRequest):
    """
    Legacy standardized endpoint for agent invocation.
    Matches the pattern expected by verification scripts.
    """
    service = get_orchestration_service()
    
    # Validate agent availability
    defn = next((d for d in service.definitions if d["id"] == request.agent_id), None)
    if not defn:
        raise HTTPException(status_code=404, detail=f"Agent '{request.agent_id}' not found")

    # The service expects the action/data/context split in the payload
    # But legacy script sends it as a nested "payload" object
    result = await service.invoke_agent(request.agent_id, request.payload)
    
    if "error" in result:
        error_msg = result["error"]
        if "System Halted" in error_msg:
            raise HTTPException(status_code=503, detail=result)
        raise HTTPException(status_code=500, detail=result)
        
    return result
