
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.agent_orchestration_service import AgentOrchestrationService

# Mock data for agent definitions
MOCK_DEFINITIONS = [
    {"id": "agent_1", "dept_id": 1, "role": "Analyst"},
    {"id": "agent_2", "dept_id": 2, "role": "Trader"}
]

@pytest.fixture
def orchestration_service():
    # Reset singleton execution for test isolation
    AgentOrchestrationService._instance = None
    
    with patch('services.agent_orchestration_service.EventBusService'), \
         patch('services.agent_orchestration_service.get_circuit_breaker') as MockCB, \
         patch('builtins.open', new_callable=MagicMock), \
         patch('json.load', return_value=MOCK_DEFINITIONS), \
         patch('os.path.exists', return_value=True):
        
        service = AgentOrchestrationService()
        # Mock circuit breaker to allow execution
        service.circuit_breaker.is_halted.return_value = False
        return service

def test_singleton_pattern():
    """Verify that the service follows singleton pattern."""
    AgentOrchestrationService._instance = None
    with patch('services.agent_orchestration_service.EventBusService'), \
         patch('services.agent_orchestration_service.get_circuit_breaker'), \
         patch('os.path.exists', return_value=False):
         
        s1 = AgentOrchestrationService()
        s2 = AgentOrchestrationService()
        assert s1 is s2

def test_load_definitions(orchestration_service):
    """Test that definitions are loaded correctly."""
    assert len(orchestration_service.definitions) == 2
    assert orchestration_service.definitions[0]["id"] == "agent_1"

def test_get_agent_creation(orchestration_service):
    """Test that get_agent lazy loads and caches agents."""
    # First call - creates agent
    with patch('services.agent_orchestration_service.DepartmentAgent') as MockAgent:
        agent1 = orchestration_service.get_agent("agent_1")
        assert agent1 is not None
        MockAgent.assert_called_once()
        
        # Second call - returns cached
        agent2 = orchestration_service.get_agent("agent_1")
        assert agent1 is agent2
        # Should still only be called once
        MockAgent.assert_called_once()

def test_get_agent_not_found(orchestration_service):
    """Test get_agent returns None for unknown IDs."""
    agent = orchestration_service.get_agent("unknown_agent")
    assert agent is None

@pytest.mark.asyncio
async def test_invoke_agent_success(orchestration_service):
    """Test successful agent invocation."""
    with patch('services.agent_orchestration_service.DepartmentAgent') as MockAgentClass:
        mock_instance = MockAgentClass.return_value
        mock_instance.invoke = AsyncMock(return_value={"status": "success"})
        
        result = await orchestration_service.invoke_agent("agent_1", {"data": "test"})
        
        assert result["status"] == "success"
        mock_instance.invoke.assert_called_once()

@pytest.mark.asyncio
async def test_invoke_agent_not_found(orchestration_service):
    """Test invocation of non-existent agent."""
    result = await orchestration_service.invoke_agent("ghost_agent", {})
    assert "error" in result
    assert result["error"] == "Agent Not Found"
