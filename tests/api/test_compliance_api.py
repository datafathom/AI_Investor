
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.compliance_api import router, get_compliance_engine, get_reporting_service
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_compliance_engine, mock_reporting_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_compliance_engine] = lambda: mock_compliance_engine
    app.dependency_overrides[get_reporting_service] = lambda: mock_reporting_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_compliance_engine():
    """Mock ComplianceEngine."""
    engine = AsyncMock()
    return engine

@pytest.fixture
def mock_reporting_service():
    """Mock ReportingService."""
    service = AsyncMock()
    return service

class FakeViolation:
    def model_dump(self, mode='json'):
        return {
            'violation_id': 'viol_1',
            'user_id': 'user_1',
            'rule_id': 'rule_1',
            'severity': 'low',
            'description': 'Test violation',
            'detected_date': '2024-01-01T12:00:00'
        }
        
    def dict(self):
        return self.model_dump()

def test_check_compliance_success(client, mock_compliance_engine):
    """Test successful compliance check."""
    
    mock_violations = [FakeViolation()]
    
    mock_compliance_engine.check_compliance.return_value = mock_violations
    
    response = client.post('/api/v1/compliance/check',
                          json={
                              'user_id': 'user_1',
                              'transaction': {}
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_check_compliance_missing_params(client):
    """Test compliance check with missing parameters."""
    response = client.post('/api/v1/compliance/check', json={'user_id': 'user_1'})
    # Transaction missing
    
    # Expect 422 Validation Error
    assert response.status_code == 422 


class FakeReport:
    def model_dump(self, mode='json'):
        return {
            'report_id': 'report_1',
            'user_id': 'user_1',
            'report_type': 'regulatory',
            'period_start': '2024-01-01T00:00:00',
            'period_end': '2024-12-31T23:59:59',
            'generated_date': '2024-01-01T12:00:00'
        }
        
    def dict(self):
        return self.model_dump()

def test_generate_report_success(client, mock_reporting_service):
    """Test successful compliance report generation."""
    mock_report = FakeReport()
    
    mock_reporting_service.generate_compliance_report.return_value = mock_report
    
    response = client.post('/api/v1/compliance/report/generate',
                          json={
                              'user_id': 'user_1',
                              'report_type': 'regulatory',
                              'period_start': '2024-01-01T00:00:00',
                              'period_end': '2024-12-31T23:59:59'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'report_id' in data['data']
