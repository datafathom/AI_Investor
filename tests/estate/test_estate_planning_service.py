"""
Tests for Estate Planning Service
Comprehensive test coverage for estate plans and beneficiary management
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.estate.estate_planning_service import EstatePlanningService
from models.estate import EstatePlan, Beneficiary, BeneficiaryType


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.estate.estate_planning_service.get_portfolio_aggregator'), \
         patch('services.estate.estate_planning_service.get_cache_service'):
        return EstatePlanningService()


@pytest.mark.asyncio
async def test_create_estate_plan(service):
    """Test estate plan creation."""
    beneficiaries = [
        {'name': 'John Doe', 'relationship': 'spouse', 'allocation_pct': 0.5},
        {'name': 'Jane Doe', 'relationship': 'child', 'allocation_pct': 0.5}
    ]
    service._save_estate_plan = AsyncMock()
    
    result = await service.create_estate_plan(
        user_id="user_123",
        beneficiaries=beneficiaries
    )
    
    assert result is not None
    assert isinstance(result, EstatePlan)
    assert len(result.beneficiaries) == 2


@pytest.mark.asyncio
async def test_calculate_estate_tax(service):
    """Test estate tax calculation."""
    estate_value = 15000000.0  # Above exemption
    
    result = await service.calculate_estate_tax(estate_value)
    
    assert result is not None
    assert 'federal_tax' in result or hasattr(result, 'federal_tax')
    assert result.get('federal_tax', 0) > 0  # Should have tax above exemption
