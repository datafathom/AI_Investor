import pytest
from flask import Flask
from web.api.institutional_api import institutional_bp
from unittest.mock import patch, MagicMock, AsyncMock
from models.institutional import Client, ClientAnalytics
from datetime import datetime

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(institutional_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('web.api.institutional_api.login_required', lambda x: x)
@patch('web.api.institutional_api.get_institutional_service')
def test_get_clients_api(mock_service, client, app):
    """Test GET /api/institutional/clients endpoint."""
    mock_instance = MagicMock()
    mock_instance.get_clients_for_advisor = AsyncMock(return_value=[
        Client(
            client_id='c1', 
            advisor_id='a1', 
            client_name='Test Client', 
            aum=1000, 
            risk_level='Low', 
            kyc_status='Verified',
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
    ])
    mock_service.return_value = mock_instance
    
    with app.app_context():
        from flask import g
        g.user_id = 'test_advisor'
        response = client.get('/api/institutional/clients')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1

@patch('web.api.institutional_api.login_required', lambda x: x)
@patch('web.api.institutional_api.get_institutional_service')
def test_get_analytics_api(mock_service, client, app):
    """Test GET /api/institutional/analytics/<client_id> endpoint."""
    mock_instance = MagicMock()
    mock_instance.get_client_analytics = AsyncMock(return_value=ClientAnalytics(
        client_id='c1', 
        fee_forecast=100.0, 
        churn_probability=0.1,
        kyc_risk_score=10.0,
        rebalance_drift=0.05,
        last_updated=datetime.utcnow()
    ))
    mock_service.return_value = mock_instance
    
    with app.app_context():
        response = client.get('/api/institutional/analytics/c1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['fee_forecast'] == 100.0
