
import pytest
from services.billing.payment_service import PaymentService
from unittest.mock import patch, MagicMock

@pytest.fixture
def service():
    # Force simulation mode for tests
    PaymentService._instance = None
    return PaymentService()

def test_create_checkout_session_simulated(service):
    session = service.create_checkout_session("user_123", "pro")
    assert "sim_user_123_pro" in session['url']
    assert session['simulated'] is True

def test_subscription_status_mock(service):
    status = service.get_subscription_status("user_123")
    assert status['tier'] == 'FREE'
    assert 'features' in status

def test_webhook_simulation_ignore(service):
    result = service.handle_webhook(b"{}", "sig")
    assert result['status'] == 'ignored'
