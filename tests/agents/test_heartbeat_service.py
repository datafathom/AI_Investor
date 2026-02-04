
import pytest
import asyncio
from datetime import timezone, datetime, timedelta
from services.agents.heartbeat_service import HeartbeatService, AgentStatus

@pytest.fixture
def heartbeat_service():
    return HeartbeatService()

@pytest.mark.asyncio
async def test_record_heartbeat(heartbeat_service):
    await heartbeat_service.record_heartbeat("agent-1", "alive")
    assert heartbeat_service.is_agent_alive("agent-1") is True
    
    agents = await heartbeat_service.get_all_agents()
    assert len(agents) == 1
    assert agents[0]["agent_id"] == "agent-1"
    assert agents[0]["status"] == "alive"

@pytest.mark.asyncio
async def test_heartbeat_timeout(heartbeat_service):
    # Manually set a stale heartbeat
    heartbeat_service._heartbeats["agent-1"] = datetime.now(timezone.utc) - timedelta(seconds=10)
    heartbeat_service._statuses["agent-1"] = AgentStatus.ALIVE
    
    # Should be dead now
    assert heartbeat_service.is_agent_alive("agent-1") is False
    
    agents = await heartbeat_service.get_all_agents()
    assert agents[0]["status"] == "dead"
    assert agents[0]["is_alive"] is False

@pytest.mark.asyncio
async def test_explicit_dead_status(heartbeat_service):
    await heartbeat_service.record_heartbeat("agent-1", "dead")
    assert heartbeat_service.is_agent_alive("agent-1") is False
