
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

@pytest.fixture
def mock_auth():
    """Mock authentication decorators before importing the blueprint."""
    def identity(f): return f
    def identity_role(role): return identity
    
    with patch('web.auth_utils.login_required', identity), \
         patch('web.auth_utils.requires_role', identity_role):
        yield

@pytest.fixture
def app(mock_auth):
    """Create Flask app for testing."""
    from web.api.risk_api import risk_bp
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(risk_bp)
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def mock_risk_monitor():
    """Mock RiskMonitor."""
    with patch('web.api.risk_api.get_risk_monitor') as mock:
        monitor = MagicMock()
        monitor.calculate_sentiment_multiplier.return_value = 1.0
        monitor.MAX_POSITION_SIZE_USD = 10000.0
        monitor.MAX_DAILY_LOSS_USD = 5000.0
        monitor.analyze_trade_risk.return_value = {'risk_score': 0.5, 'approved': True}
        mock.return_value = monitor
        yield monitor

@pytest.fixture
def mock_circuit_breaker():
    """Mock CircuitBreaker."""
    with patch('web.api.risk_api.get_circuit_breaker') as mock:
        breaker = MagicMock()
        breaker.is_halted.return_value = False
        breaker.freeze_reason = "No reason"
        mock.return_value = breaker
        yield breaker

def test_get_risk_status_success(client, mock_risk_monitor, mock_circuit_breaker):
    """Test successful risk status retrieval."""
    with patch('web.api.risk_api.get_fear_greed_service') as mock_fg:
        service_instance = MagicMock()
        service_instance.get_fear_greed_index.return_value = {
            'score': 50,
            'label': 'neutral'
        }
        mock_fg.return_value = service_instance
        response = client.get('/status')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'halted' in data
        assert 'sentiment' in data

def test_toggle_kill_switch_engage_success(client, mock_circuit_breaker):
    """Test successful kill switch engagement."""
    with patch('web.api.risk_api.get_totp_service') as mock_totp:
        mock_totp.return_value.verify_code.return_value = True
        response = client.post('/kill-switch',
                              json={
                                  'action': 'engage',
                                  'reason': 'Test',
                                  'mfa_code': '123456'
                              })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'HALTED'

def test_risk_preview_success(client, mock_risk_monitor):
    """Test successful risk preview."""
    response = client.post('/preview',
                          json={
                              'symbol': 'AAPL',
                              'side': 'buy',
                              'quantity': 100,
                              'price': 150.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'risk_score' in data or 'approved' in data
