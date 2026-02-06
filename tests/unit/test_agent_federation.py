"""
Unit tests for Agent Federation (Delegation) capability.
Tests the request_help() flow between agents.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.fixture
def mock_orchestrator():
    """Create a mock orchestrator for delegation tests."""
    with patch('services.agent_orchestration_service.get_orchestration_service') as mock_get:
        mock_service = MagicMock()
        mock_service.invoke_agent = AsyncMock(return_value={
            "agent": "target_agent",
            "status": "success",
            "response": "Delegation completed"
        })
        mock_get.return_value = mock_service
        yield mock_service


@pytest.fixture
def source_agent():
    """Create a concrete agent for testing (not abstract)."""
    from agents.department_agent import DepartmentAgent
    with patch('agents.department_agent.EventBusService'):
        agent = DepartmentAgent(name="test_source", dept_id=1, role="Analyst")
        return agent


@pytest.mark.asyncio
async def test_request_help_calls_orchestrator(source_agent, mock_orchestrator):
    """Test that request_help properly delegates to orchestrator."""
    result = await source_agent.request_help(
        agent_id="target_agent",
        sub_task="Analyze market trends",
        context={"ticker": "AAPL"}
    )
    
    # Verify orchestrator was called with correct payload
    mock_orchestrator.invoke_agent.assert_called_once()
    call_args = mock_orchestrator.invoke_agent.call_args
    assert call_args[0][0] == "target_agent"
    assert call_args[0][1]["action"] == "Analyze market trends"
    assert call_args[0][1]["requester"] == "test_source"
    
    # Verify result is returned
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_request_help_with_empty_context(source_agent, mock_orchestrator):
    """Test request_help works with no context provided."""
    result = await source_agent.request_help(
        agent_id="target_agent",
        sub_task="Simple task"
    )
    
    call_args = mock_orchestrator.invoke_agent.call_args
    assert call_args[0][1]["data"] == {}
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_delegation_api_endpoint():
    """Test the /delegate API endpoint."""
    from fastapi.testclient import TestClient
    from web.api.agents_api import router
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(router)
    
    with patch('web.api.agents_api.get_orchestration_service') as mock_get:
        mock_service = MagicMock()
        mock_service.definitions = [
            {"id": "agent_a", "dept_id": 1, "role": "Source"},
            {"id": "agent_b", "dept_id": 2, "role": "Target"}
        ]
        
        # Mock agent instance
        mock_agent = MagicMock()
        mock_agent.request_help = AsyncMock(return_value={
            "status": "success",
            "response": "Task delegated"
        })
        mock_service.get_agent.return_value = mock_agent
        mock_get.return_value = mock_service
        
        client = TestClient(app)
        response = client.post("/api/v1/agents/delegate", json={
            "source_agent": "agent_a",
            "target_agent": "agent_b",
            "sub_task": "Review document",
            "context": {"doc_id": "123"}
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["delegation"]["source"] == "agent_a"
        assert data["delegation"]["target"] == "agent_b"
        assert data["result"]["status"] == "success"


@pytest.mark.asyncio
async def test_delegation_api_source_not_found():
    """Test that delegation fails when source agent doesn't exist."""
    from fastapi.testclient import TestClient
    from web.api.agents_api import router
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(router)
    
    with patch('web.api.agents_api.get_orchestration_service') as mock_get:
        mock_service = MagicMock()
        mock_service.definitions = [{"id": "agent_b", "dept_id": 2, "role": "Target"}]
        mock_get.return_value = mock_service
        
        client = TestClient(app)
        response = client.post("/api/v1/agents/delegate", json={
            "source_agent": "nonexistent",
            "target_agent": "agent_b",
            "sub_task": "Test"
        })
        
        assert response.status_code == 404
        assert "nonexistent" in response.json()["detail"]
