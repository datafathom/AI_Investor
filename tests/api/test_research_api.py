"""
Tests for Research API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.research_api import router, get_research_provider, get_report_generator_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_research_service(api_app):
    """Mock Research Service."""
    service = AsyncMock()
    
    report = MagicMock()
    report.model_dump.return_value = {"id": "rep_123", "title": "Test Report", "status": "completed"}
    
    service.generate_portfolio_report.return_value = report
    service.generate_company_research.return_value = report
    service._get_reports_from_db.return_value = [report]
    
    api_app.dependency_overrides[get_research_provider] = lambda: service
    return service


@pytest.fixture
def mock_generator(api_app):
    """Mock Report Generator."""
    service = AsyncMock()
    service.generate_pdf.return_value = b"%PDF-1.4"
    service.generate_html.return_value = "<html></html>"
    service.generate_excel.return_value = b"excel-data"
    
    api_app.dependency_overrides[get_report_generator_provider] = lambda: service
    return service


def test_generate_portfolio_report_success(client, mock_research_service):
    """Test generating portfolio report."""
    payload = {"user_id": "user_1", "portfolio_id": "port_123", "title": "Portfolio Alpha"}
    response = client.post('/api/v1/research/portfolio-report', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['id'] == "rep_123"


def test_generate_company_research_success(client, mock_research_service):
    """Test generating company research."""
    payload = {"user_id": "user_1", "symbol": "AAPL", "title": "Apple Dive"}
    response = client.post('/api/v1/research/company-research', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_get_user_reports_success(client, mock_research_service):
    """Test getting user reports."""
    response = client.get('/api/v1/research/reports?user_id=user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_templates_success(client):
    """Test getting templates."""
    response = client.get('/api/v1/research/templates')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 3


def test_download_pdf_success(client, mock_generator):
    """Test downloading PDF."""
    response = client.get('/api/v1/research/report/rep_123/pdf')
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'
    assert b"%PDF-1.4" in response.content


def test_download_html_success(client, mock_generator):
    """Test downloading HTML."""
    response = client.get('/api/v1/research/report/rep_123/html')
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    assert "<html></html>" in response.text
