"""
Tests for Compliance Reporting Service
Comprehensive test coverage for automated report generation and regulatory filings
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, AsyncMock, patch
from services.compliance.reporting_service import ReportingService
from models.compliance import ComplianceReport


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.compliance.reporting_service.get_compliance_engine'), \
         patch('services.compliance.reporting_service.get_cache_service'):
        return ReportingService()


@pytest.mark.asyncio
async def test_generate_compliance_report(service):
    """Test compliance report generation."""
    service.compliance_engine.get_violations = AsyncMock(return_value=[])
    service._save_report = AsyncMock()
    
    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)
    
    result = await service.generate_compliance_report(
        user_id="user_123",
        report_type="annual",
        period_start=start_date,
        period_end=end_date
    )
    
    assert result is not None
    assert isinstance(result, ComplianceReport)
    assert result.user_id == "user_123"
    assert result.report_type == "annual"
    assert result.period_start == start_date
    assert result.period_end == end_date


@pytest.mark.asyncio
async def test_generate_regulatory_filing(service):
    """Test regulatory filing generation."""
    service._generate_filing_content = AsyncMock(return_value="Filing content...")
    service._save_filing = AsyncMock()
    
    result = await service.generate_regulatory_filing(
        user_id="user_123",
        filing_type="sec_form_13f",
        period_end=datetime(2024, 12, 31, tzinfo=timezone.utc)
    )
    
    assert result is not None
    assert 'filing_id' in result or hasattr(result, 'filing_id')
