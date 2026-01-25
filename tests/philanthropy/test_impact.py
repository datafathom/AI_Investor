"""
Tests for Phase 61: Philanthropy & Impact
Verifies DonationService, ESGService logic.
"""
import pytest
from services.philanthropy.donation_service import DonationService
from services.analysis.esg_service import ESGService

@pytest.mark.asyncio
async def test_donation_logic():
    service = DonationService()
    
    # Test excess calculation
    excess = await service.calculate_excess_alpha(3500000, 3000000)
    assert excess == 500000
    
    # Test routing
    allocations = [{"category": "Climate", "percentage": 100}]
    record = await service.route_excess_alpha(10000, allocations)
    
    assert record.total_amount == 10000
    assert record.tax_savings_est == 3500 # 35%
    assert len(service._history) == 1

@pytest.mark.asyncio
async def test_esg_logic():
    service = ESGService()
    
    # Test scores
    scores = await service.get_portfolio_esg_scores()
    assert 0 <= scores.composite <= 100
    
    # Test carbon
    footprint = await service.calculate_carbon_footprint(1000000)
    assert footprint.total_emissions_tons == 95.0
    
    # Test sin stocks
    sins = await service.detect_sin_stocks()
    assert isinstance(sins, list)
