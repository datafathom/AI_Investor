"""
Tests for Research & Reports API Endpoints
Phase 18: Research Reports & Generation
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.research_api import research_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(research_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_research_service():
    """Mock ResearchService."""
    with patch('web.api.research_api.get_research_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_report_generator():
    """Mock ReportGenerator."""
    with patch('web.api.research_api.get_report_generator') as mock:
        generator = AsyncMock()
        mock.return_value = generator
        yield generator


def test_generate_portfolio_report_success(client, mock_research_service):
    """Test successful portfolio report generation."""
    from models.research import ResearchReport, ReportType, ReportStatus
    from datetime import datetime, timezone
    
    mock_report = ResearchReport(
        report_id='report_1',
        user_id='user_1',
        report_type=ReportType.PORTFOLIO_ANALYSIS,
        title='Portfolio Analysis Report',
        content='Sample report content.',
        sections=[],
        charts=[],
        data={},
        status=ReportStatus.COMPLETED,
        generated_date=datetime.now(timezone.utc),
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_research_service.generate_portfolio_report.return_value = mock_report
    
    response = client.post('/api/v1/research/portfolio-report',
                          json={
                              'user_id': 'user_1',
                              'portfolio_id': 'portfolio_1',
                              'title': 'Portfolio Analysis Report'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['report_id'] == 'report_1'


def test_generate_portfolio_report_missing_params(client):
    """Test portfolio report generation with missing parameters."""
    response = client.post('/api/v1/research/portfolio-report',
                          json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_generate_company_research_success(client, mock_research_service):
    """Test successful company research generation."""
    from models.research import ResearchReport, ReportType, ReportStatus
    from datetime import datetime, timezone
    
    mock_report = ResearchReport(
        report_id='report_1',
        user_id='user_1',
        report_type=ReportType.COMPANY_RESEARCH,
        title='Company Research Report',
        content='Sample company research content.',
        sections=[],
        charts=[],
        data={},
        status=ReportStatus.COMPLETED,
        generated_date=datetime.now(timezone.utc),
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_research_service.generate_company_research.return_value = mock_report
    
    response = client.post('/api/v1/research/company-research',
                          json={
                              'user_id': 'user_1',
                              'symbol': 'AAPL',
                              'title': 'Company Research Report'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

