
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agents.department_agent import DepartmentAgent

@pytest.fixture
def mock_department_agent():
    with patch('agents.department_agent.EventBusService') as MockEventBus:
        agent = DepartmentAgent(name="test_agent", dept_id=1, role="Test Role")
        # Mock the get_completion method from BaseAgent
        agent.get_completion = AsyncMock(return_value="Mocked LLM Response")
        return agent

@pytest.mark.asyncio
async def test_invoke_success(mock_department_agent):
    """Test successful invocation of an agent."""
    payload = {"action": "analyze", "data": "financial_data"}
    
    # Mock _load_prompt to return simple templates
    with patch.object(mock_department_agent, '_load_prompt', side_effect=lambda x: "Template: {action} {context}" if "user" in x else "System: {role}"):
        result = await mock_department_agent.invoke(payload)
        
        assert result["status"] == "success"
        assert result["response"] == "Mocked LLM Response"
        assert result["agent"] == "test_agent"
        
        # Verify event bus was published to
        mock_department_agent.event_bus.publish.assert_called_once()
        args, _ = mock_department_agent.event_bus.publish.call_args
        assert args[0] == "dept.1.agents"
        assert args[1]["response"] == "Mocked LLM Response"

@pytest.mark.asyncio
async def test_invoke_error_handling(mock_department_agent):
    """Test invoke method error handling."""
    mock_department_agent.get_completion.side_effect = Exception("LLM Error")
    
    with patch.object(mock_department_agent, '_load_prompt', return_value=""):
        result = await mock_department_agent.invoke({"action": "fail"})
        
        assert result["status"] == "error"
        assert "LLM Error" in result["error"]

@pytest.mark.asyncio
async def test_process_event_telemetry(mock_department_agent):
    """Test that process_event returns telemetry."""
    mock_department_agent.start() # Ensure active
    event = {"type": "market_tick"}
    
    result = mock_department_agent.process_event(event)
    
    assert result["type"] == "agent_telemetry"
    assert result["status"] == "busy"
    assert "market_tick" in result["message"]
