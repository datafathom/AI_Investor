import pytest
import asyncio
from typing import Dict, Any, Optional
from services.mission_service import get_mission_service
from agents.base_agent import BaseAgent
from agents.tools_registry import BaseTool, get_tool_registry, BaseModel, Field

# --- Mocks ---
class MockToolShadow(BaseTool):
    name = "shadow_exploit"
    description = "A restricted tool."
    class Args(BaseModel):
        target: str = Field(..., description="Target to exploit")
    args_schema = Args
    def run(self, args): return "Exploited"

class MockAgent(BaseAgent):
    def process_event(self, event): pass

# Register Mock Tool
get_tool_registry().register(MockToolShadow)

# --- Tests ---

@pytest.mark.asyncio
async def test_mission_deployment_logic():
    service = get_mission_service()
    
    # 1. Load Template
    template = service.get_template("mission_001") # M&A Scout
    assert template is not None
    assert template["sector"] == "Wealth"
    
    # 2. Deploy (Simulation without ARQ)
    # We pass None for arq_pool to trigger simulation mode logging
    deployment = await service.deploy_mission("mission_001", {"budget": 1000}, None)
    
    assert deployment["status"] == "deployed"
    assert "mssn_" in deployment["mission_id"]
    assert deployment["context"]["budget_limit"] == 1000
    assert deployment["context"]["goal"] == template["goal"]

@pytest.mark.asyncio
async def test_sector_isolation_enforcement():
    # 1. Create a "Wealth" agent (Regular)
    wealth_agent = MockAgent(name="wealth_analyst_01")
    
    # 2. Attempt to use Shadow Tool
    # Should FAIL
    result = await wealth_agent.execute_tool("shadow_exploit", {"target": "competitor"})
    assert "Security Violation" in result or "access denied" in result
    
    # 3. Create a "Shadow" agent
    shadow_agent = MockAgent(name="shadow_operative_01")
    
    # 4. Attempt to use Shadow Tool
    # Should SUCCEED
    result_success = await shadow_agent.execute_tool("shadow_exploit", {"target": "competitor"})
    assert result_success == "Exploited"
