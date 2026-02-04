"""
Tests for Report Generator
Comprehensive test coverage for PDF, HTML, and Excel report generation
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.research.report_generator import ReportGenerator
from schemas.research import ResearchReport, ReportType, ReportStatus


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.research.report_generator.get_research_service'), \
         patch('services.research.report_generator.get_cache_service'):
        return ReportGenerator()


@pytest.fixture
def mock_report():
    """Mock research report."""
    return ResearchReport(
        report_id="report_123",
        user_id="user_123",
        report_type=ReportType.PORTFOLIO_ANALYSIS,
        title="Test Report",
        content="Report content here...",
        status=ReportStatus.COMPLETED,
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )


@pytest.mark.asyncio
async def test_generate_pdf(service, mock_report):
    """Test PDF report generation."""
    service.research_service._get_report = AsyncMock(return_value=mock_report)
    
    result = await service.generate_pdf("report_123")
    
    assert result is not None
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_generate_html(service, mock_report):
    """Test HTML report generation."""
    service.research_service._get_report = AsyncMock(return_value=mock_report)
    
    result = await service.generate_html("report_123")
    
    assert result is not None
    assert isinstance(result, str)
    assert "<html" in result.lower() or "html" in result.lower()


@pytest.mark.asyncio
async def test_generate_excel(service, mock_report):
    """Test Excel report generation."""
    service.research_service._get_report = AsyncMock(return_value=mock_report)
    
    result = await service.generate_excel("report_123")
    
    assert result is not None
    assert isinstance(result, bytes)


@pytest.mark.asyncio
async def test_generate_pdf_report_not_found(service):
    """Test PDF generation with non-existent report."""
    service.research_service._get_report = AsyncMock(return_value=None)
    
    with pytest.raises(ValueError, match="not found"):
        await service.generate_pdf("nonexistent")
