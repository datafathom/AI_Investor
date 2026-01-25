
import pytest
from unittest.mock import patch, MagicMock
from services.system.alert_service import AlertService, get_alert_service

@pytest.fixture
def alert_service():
    # Reset singleton
    AlertService._instance = None
    # Patch the local reference in the alert_service module
    with patch('services.system.alert_service.get_secret_manager') as mock_sm:
        mock_sm.return_value.get_secret.side_effect = lambda k, default=None: {
            'SLACK_WEBHOOK_URL': 'https://mock.slack.com/hook',
            'PAGERDUTY_ROUTING_KEY': 'pd-key'
        }.get(k, default)
        return AlertService()

def test_singleton():
    # Ensure singleton behaves correctly across calls
    with patch('services.system.alert_service.get_secret_manager'):
        s1 = get_alert_service()
        s2 = get_alert_service()
        assert s1 is s2

@patch('requests.post')
def test_trigger_alert(mock_post, alert_service):
    alert_service.trigger_alert("abc", "def", "warning")
    
    assert mock_post.called
    _, kwargs = mock_post.call_args
    sent_payload = kwargs.get('json', {})
    assert "abc" in sent_payload.get('text', '')
    assert "def" in sent_payload.get('text', '')
    assert "WARNING" in sent_payload.get('text', '')
