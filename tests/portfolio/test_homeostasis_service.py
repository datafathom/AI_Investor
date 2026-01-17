
import unittest
from unittest.mock import patch, MagicMock
from services.portfolio.homeostasis_service import HomeostasisService

class TestHomeostasisService(unittest.TestCase):
    def setUp(self):
        self.service = HomeostasisService()
        self.service.homeostasis_target = 1000000.0
        self.tenant_id = "test_tenant"

    def test_homeostasis_score_calculation(self):
        """Verify the progress score towards 'Enough'."""
        self.service.update_net_worth(self.tenant_id, 500000.0)
        status = self.service.get_homeostasis_status(self.tenant_id)
        self.assertEqual(status["homeostasis_score"], 50.0)
        self.assertFalse(status["preservation_mode"])

    def test_preservation_mode_trigger(self):
        """Verify that reaching the target engages preservation mode."""
        self.service.update_net_worth(self.tenant_id, 1200000.0)
        status = self.service.get_homeostasis_status(self.tenant_id)
        self.assertEqual(status["homeostasis_score"], 100.0)
        self.assertTrue(status["preservation_mode"])

    @patch('services.data.bank_simulation.bank_simulator.pull_surplus')
    @patch('services.data.bank_simulation.bank_simulator.get_status')
    def test_autopilot_cash_pull(self, mock_get_status, mock_pull):
        """Verify autopilot pulls surplus from bank."""
        mock_get_status.return_value = {
            "bank_balance": 20000.0,
            "monthly_expenses": 4000.0,
            "connected": True
        }
        # Threshold is expenses * 3 = 12000. Surplus = 20000 - 12000 = 8000.
        self.service.update_net_worth(self.tenant_id, 100000.0)
        mock_pull.assert_called_with(self.tenant_id, 8000.0)

if __name__ == '__main__':
    unittest.main()
