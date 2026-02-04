"""
Tests for Professional Tools Service
Comprehensive test coverage for advanced analytics and custom reporting
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.institutional.professional_tools_service import ProfessionalToolsService
from schemas.institutional import ProfessionalReport


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.institutional.professional_tools_service.get_cache_service'):
        return ProfessionalToolsService()


@pytest.mark.asyncio
async def test_generate_professional_report(service):
    """Test professional report generation."""
    service._save_report = AsyncMock()
    
    result = await service.generate_professional_report(
        advisor_id="advisor_123",
        client_id="client_456",
        report_type="performance",
        content={'total_return': 0.15, 'sharpe_ratio': 1.2}
    )
    
    assert result is not None
    assert isinstance(result, ProfessionalReport)
    assert result.advisor_id == "advisor_123"
    assert result.client_id == "client_456"
    assert result.report_type == "performance"
