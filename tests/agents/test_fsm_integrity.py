import pytest
import asyncio
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent, AgentState
from agents.tools_registry import get_tool_registry, BaseTool
from services.infrastructure.state_manager import get_fsm_manager

# --- Mock Agent ---
class MockAgent(BaseAgent):
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return None

# --- Mock Tool ---
class MockTool(BaseTool):
    pass # Wait, need schema

# --- Test ---
@pytest.mark.asyncio
async def test_fsm_transitions():
    agent = MockAgent(name="test_agent_01")
    fsm = get_fsm_manager()
    
    # 1. Initial State
    assert agent.state == AgentState.INIT
    
    # 2. Valid Transition
    await agent.transition_to(AgentState.SCANNING, reason="Start scanning")
    assert agent.state == AgentState.SCANNING
    
    # Verify Redis persistence
    saved = fsm.load_state(agent.name)
    assert saved["state"] == AgentState.SCANNING.value
    assert saved["context"]["reason"] == "Start scanning"
    
    # 3. Invalid Transition (SCANNING -> EXECUTING is invalid, needs ANALYZING first)
    # Valid: INIT->SCANNING->ANALYZING->EXECUTING
    with pytest.raises(RuntimeError) as excinfo:
        await agent.transition_to(AgentState.EXECUTING, reason="Illegal jump")
    
    assert "FSM Security Violation" in str(excinfo.value)
    assert agent.state == AgentState.SECURITY_HALT

@pytest.mark.asyncio
async def test_state_recovery():
    agent_name = "test_agent_recovery"
    fsm = get_fsm_manager()
    
    # Simulate a saved state
    context = {"step_id": "step_99", "parent_job_id": "job_123"}
    fsm.save_state(agent_name, AgentState.ANALYZING, context)
    
    # Initialize fresh agent
    agent = MockAgent(name=agent_name)
    assert agent.state == AgentState.INIT # Defaults to INIT
    
    # Load state
    success = await agent.load_saved_state()
    assert success is True
    assert agent.state == AgentState.ANALYZING
    assert agent.step_id == "step_99"
    assert agent.parent_job_id == "job_123"

@pytest.mark.asyncio
async def test_tool_execution():
    agent = MockAgent(name="test_agent_tool")
    
    # Ensure calculator is registered (it is auto-registered on import)
    # We trigger import by importing agents.tools.calculator in the test or relying on global app load
    # Let's import it here to be safe
    import agents.tools.calculator
    
    # 1. Valid Execution
    result = await agent.execute_tool("calculator", {"operation": "add", "x": 10, "y": 5})
    assert result == 15.0
    
    # 2. Invalid Schema
    result_err = await agent.execute_tool("calculator", {"operation": "add", "x": "ten", "y": 5})
    assert "Validation Error" in str(result_err)
    
    # 3. Execution Error (Div by zero)
    result_div = await agent.execute_tool("calculator", {"operation": "divide", "x": 10, "y": 0})
    assert "Execution Error" in str(result_div)
    
    # 4. Unknown Tool
    result_unknown = await agent.execute_tool("fake_tool", {})
    assert "Tool 'fake_tool' not found" in str(result_unknown)
