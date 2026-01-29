import unittest
from unittest.mock import MagicMock, patch
from services.unified_activity_service import UnifiedActivityService
from services.price_telemetry_service import PriceTelemetryService

class TestTelemetryRebuild(unittest.TestCase):

    def setUp(self):
        self.activity_svc = UnifiedActivityService()
        self.telemetry_svc = PriceTelemetryService()

    @patch("services.unified_activity_service.SessionLocal")
    def test_activity_logging(self, mock_session_cls):
        """Test that log_activity attempts to write to DB."""
        # Mock DB session
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        
        self.activity_svc.log_activity("TEST_AGENT", "TEST_ACTION", {"data": 123})
        
        # Verify Session was created and add/commit called
        mock_session_cls.assert_called()
        mock_session.add.assert_called()
        mock_session.commit.assert_called()

    @patch("services.price_telemetry_service.SessionLocal")
    def test_price_storage(self, mock_session_cls):
        """Test storing a price tick."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        
        self.telemetry_svc.store_tick("BTC", 50000.0)
        
        # Verify execute called
        mock_session.execute.assert_called()
        mock_session.commit.assert_called()

if __name__ == '__main__':
    unittest.main()
