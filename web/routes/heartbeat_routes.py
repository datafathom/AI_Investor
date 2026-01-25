"""Routes for Agent Heartbeats."""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from services.agents.heartbeat_service import heartbeat_service
import asyncio

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])

@router.get("/status")
async def get_agent_status():
    """Get current status of all agents."""
    return await heartbeat_service.get_all_agents()

@router.get("/health")
async def health_check():
    """Simple API health check."""
    return {"status": "ok"}

# Simple endpoint for agents to push heartbeat via HTTP if Kafka is down
@router.post("/heartbeat/{agent_id}")
async def push_heartbeat(agent_id: str, status: str = "alive"):
    await heartbeat_service.record_heartbeat(agent_id, status)
    return {"status": "recorded"}
