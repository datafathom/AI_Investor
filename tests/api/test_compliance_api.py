"""
Tests for Compliance API Endpoints
Phase 25: Compliance & Regulatory Reporting
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.compliance_api import compliance_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(compliance_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_compliance_engine():
    """Mock ComplianceEngine."""
    with patch('web.api.compliance_api.get_compliance_engine') as mock:
        engine = AsyncMock()
        mock.return_value = engine
        yield engine


@pytest.fixture
def mock_reporting_service():
    """Mock ReportingService."""
    with patch('web.api.compliance_api.get_reporting_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_check_compliance_success(client, mock_compliance_engine):
    """Test successful compliance check."""
    from models.compliance import ComplianceViolation
    
    mock_violations = [
        ComplianceViolation(
            violation_id='viol_1',
            user_id='user_1',
            rule_id='rule_1',
            severity='low',
            description='Test violation'
        )
    ]
    mock_compliance_engine.check_compliance.return_value = mock_violations
    
    response = client.post('/api/compliance/check',
                          json={
                              'user_id': 'user_1',
                              'transaction': {}
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_check_compliance_missing_params(client):
    """Test compliance check with missing parameters."""
    response = client.post('/api/compliance/check', json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_generate_report_success(client, mock_reporting_service):
    """Test successful compliance report generation."""
    from models.compliance import ComplianceReport
    
    mock_report = ComplianceReport(
        report_id='report_1',
        user_id='user_1',
        report_type='regulatory',
        status='completed'
    )
    mock_reporting_service.generate_report.return_value = mock_report
    
    response = client.post('/api/compliance/report/generate',
                          json={
                              'user_id': 'user_1',
                              'report_type': 'regulatory',
                              'period_start': '2024-01-01',
                              'period_end': '2024-12-31'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
