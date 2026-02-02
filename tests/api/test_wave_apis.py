"""
Tests for Wave APIs (Consolidated Endpoints)
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from flask import Flask
from web.api.wave_apis import (
    backtest_bp, estate_bp, compliance_bp, scenario_bp,
    philanthropy_bp, system_bp, corporate_bp, margin_bp,
    mobile_bp, integrations_bp, assets_bp, zen_bp
)


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(backtest_bp)
    app.register_blueprint(estate_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(scenario_bp)
    app.register_blueprint(philanthropy_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(corporate_bp)
    app.register_blueprint(margin_bp)
    app.register_blueprint(mobile_bp)
    app.register_blueprint(integrations_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(zen_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_backtest_monte_carlo_success(client):
    """Test successful Monte Carlo simulation."""
    with patch('web.api.wave_apis.get_monte_carlo_service') as mock:
        service = AsyncMock()
        from services.analysis.monte_carlo_service import SimulationResult
        mock_result = SimulationResult(
            paths=[[1000000.0, 1050000.0]],
            quantiles={'p10': [900000.0]},
            ruin_probability=0.05,
            median_final=1100000.0,
            mean_final=1105000.0
        )
        service.run_gbm_simulation.return_value = mock_result
        mock.return_value = service
        
        response = client.post('/monte-carlo',
                              json={
                                  'initial_value': 1000000,
                                  'mu': 0.08,
                                  'sigma': 0.15
                              })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'paths' in data['data']
        assert 'ruin_probability' in data['data']


def test_estate_heartbeat_success(client):
    """Test successful estate heartbeat."""
    with patch('web.api.wave_apis.get_estate_service') as mock:
        service = AsyncMock()
        from services.security.estate_service import HeartbeatStatus
        mock_status = HeartbeatStatus(
            last_check='2024-01-01',
            is_alive=True,
            days_until_trigger=365,
            trigger_date='2025-01-01'
        )
        service.check_heartbeat.return_value = mock_status
        mock.return_value = service
        
        response = client.get('/heartbeat')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'is_alive' in data['data']
        assert 'days_until_trigger' in data['data']


def test_compliance_overview_success(client):
    """Test successful compliance overview."""
    with patch('web.api.wave_apis.get_compliance_service') as mock:
        service = AsyncMock()
        service.get_compliance_score.return_value = 0.95
        service.get_sar_alerts.return_value = []
        service.get_audit_logs.return_value = []
        mock.return_value = service
        
        response = client.get('/overview')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'compliance_score' in data['data']
        assert 'pending_alerts' in data['data']
