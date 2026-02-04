"""
Tests for Research Service
Comprehensive test coverage for research report generation
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.research.research_service import ResearchService
from schemas.research import ResearchReport, ReportType, ReportStatus


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.research.research_service.get_cache_service'):
        return ResearchService()


@pytest.mark.asyncio
async def test_generate_portfolio_report(service):
    """Test portfolio report generation."""
    service._generate_portfolio_content = AsyncMock(return_value="Portfolio analysis content...")
    service._generate_portfolio_sections = AsyncMock(return_value=[
        {'title': 'Overview', 'content': 'Portfolio overview'},
        {'title': 'Performance', 'content': 'Performance analysis'}
    ])
    service._collect_portfolio_data = AsyncMock(return_value={'total_value': 100000.0})
    service._save_report = AsyncMock()
    
    result = await service.generate_portfolio_report(
        user_id="user_123",
        portfolio_id="portfolio_123"
    )
    
    assert result is not None
    assert isinstance(result, ResearchReport)
    assert result.report_type == ReportType.PORTFOLIO_ANALYSIS
    assert result.status == ReportStatus.COMPLETED


@pytest.mark.asyncio
async def test_generate_company_report(service):
    """Test company research report generation."""
    service._generate_company_content = AsyncMock(return_value="Company analysis...")
    service._generate_company_sections = AsyncMock(return_value=[])
    service._collect_company_data = AsyncMock(return_value={})
    service._save_report = AsyncMock()
    
    result = await service.generate_company_report(
        user_id="user_123",
        symbol="AAPL"
    )
    
    assert result is not None
    assert result.report_type == ReportType.COMPANY_RESEARCH


@pytest.mark.asyncio
async def test_get_reports(service):
    """Test getting user reports."""
    service._get_reports_from_db = AsyncMock(return_value=[
        ResearchReport(
            report_id="report_1",
            user_id="user_123",
            report_type=ReportType.PORTFOLIO_ANALYSIS,
            title="Report 1",
            content="Content",
            status=ReportStatus.COMPLETED,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
    ])
    
    result = await service.get_reports("user_123")
    
    assert result is not None
    assert len(result) == 1


@pytest.mark.asyncio
async def test_generate_portfolio_report_error_handling(service):
    """Test error handling in report generation."""
    service._generate_portfolio_content = AsyncMock(side_effect=Exception("Error"))
    
    with pytest.raises(Exception):
        await service.generate_portfolio_report(
            user_id="user_123",
            portfolio_id="portfolio_123"
        )
