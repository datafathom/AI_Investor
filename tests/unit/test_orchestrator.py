import unittest
from services.neo4j.master_graph import MasterGraphService
from services.infrastructure.event_bus import EventBusService
from services.ai.master_objective import MasterObjectiveService
from services.admin.command_center_svc import CommandCenterService

class TestAIWealthOrchestrator(unittest.TestCase):

    def setUp(self):
        self.graph_svc = MasterGraphService()
        self.event_bus = EventBusService()
        self.objective_svc = MasterObjectiveService()
        self.command_svc = CommandCenterService()

    def test_master_graph_unification(self):
        """Test the brain's ability to merge graphs."""
        result = self.graph_svc.unify_graphs()
        self.assertTrue(result)
        
        exposure = self.graph_svc.query_global_exposure("Geopolitical Risk")
        self.assertTrue(len(exposure) > 0)

    def test_event_bus_reflex(self):
        """Test global nervous system reflex."""
        self.reflex_triggered = False
        
        def margin_call_handler(payload):
            self.reflex_triggered = True
            self.assertEqual(payload['severity'], 'HIGH')
            
        self.event_bus.subscribe("MARGIN_CALL_RISK", margin_call_handler)
        self.event_bus.publish("MARGIN_CALL_RISK", {"severity": "HIGH", "cause": "Market Crash"})
        
        self.assertTrue(self.reflex_triggered)

    def test_master_objective(self):
        """Test ROL calculations."""
        # $10M wealth, $200k burn, 0.9 happiness
        rol = self.objective_svc.calculate_rol(10000000, 200000, 0.9)
        # 50 years * 0.9 = 45
        self.assertEqual(rol, 45.0)
        
        # Survival Check
        # 5% liquidity (Fail), 10% VaR (Pass) -> Overall Fail
        safe = self.objective_svc.check_survival_constraint(0.05, 0.10)
        self.assertFalse(safe)

    def test_command_center(self):
        """Test God Mode aggregation."""
        status = self.command_svc.get_system_status()
        self.assertEqual(status['orchestrator_status'], "ONLINE")
        self.assertEqual(status['active_phases'], 200)

if __name__ == '__main__':
    unittest.main()
