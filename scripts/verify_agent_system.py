import asyncio
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.agent_orchestration_service import AgentOrchestrationService
from agents.department_agent import DepartmentAgent

class TestAgentSystem(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mocking external dependencies
        self.patcher_db = patch("services.department_service.SessionLocal")
        self.mock_db = self.patcher_db.start()
        
        # Reset singleton for testing
        AgentOrchestrationService._instance = None
        self.service = AgentOrchestrationService()

    def tearDown(self):
        self.patcher_db.stop()

    def test_definitions_loaded(self):
        """Check if all 108 agents are loaded."""
        self.assertEqual(len(self.service.definitions), 108)
        print(f"✓ Verified 108 agent definitions loaded.")

    def test_agent_lazy_loading(self):
        """Verify an agent instance is created correctly."""
        agent_id = "synthesizer"
        agent = self.service.get_agent(agent_id)
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, agent_id)
        self.assertEqual(agent.dept_id, 1)
        self.assertTrue(agent.is_active)
        print(f"✓ Verified lazy loading for agent: {agent_id}")

    @patch("agents.department_agent.DepartmentAgent.get_completion")
    async def test_agent_invocation(self, mock_completion):
        """Test the end-to-end invocation flow."""
        mock_completion.return_value = "Verified response from agent."
        
        agent_id = "sniper" # Trader Dept
        payload = {"action": "scan", "data": {"pair": "BTC/USD"}}
        
        result = await self.service.invoke_agent(agent_id, payload)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["response"], "Verified response from agent.")
        self.assertEqual(result["agent"], agent_id)
        print(f"✓ Verified invocation for agent: {agent_id}")

    def test_circuit_breaker_integration(self):
        """Ensure invocation fails if system is halted."""
        from services.risk.circuit_breaker import get_circuit_breaker
        cb = get_circuit_breaker()
        cb.trigger_global_kill_switch("Test Halted")
        
        # This is a sync test of the logic check
        async def run_inv():
            return await self.service.invoke_agent("synthesizer", {})
            
        result = asyncio.run(run_inv())
        self.assertEqual(result["error"], "System Halted")
        
        cb.reset() # Reset for other tests
        print(f"✓ Verified circuit breaker integration.")

if __name__ == "__main__":
    unittest.main()
