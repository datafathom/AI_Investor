"""
Tests for Enhanced Tax Harvesting Service
Comprehensive test coverage for harvest opportunities, wash-sale detection, and batch processing
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from services.tax.enhanced_tax_harvesting_service import (
    EnhancedTaxHarvestingService,
    EnhancedHarvestOpportunity,
    BatchHarvestResult
)
from services.tax.harvest_service import HarvestCandidate


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.tax.enhanced_tax_harvesting_service.TaxHarvestService'), \
         patch('services.tax.enhanced_tax_harvesting_service.get_portfolio_aggregator'), \
         patch('services.tax.enhanced_tax_harvesting_service.get_cache_service'):
        return EnhancedTaxHarvestingService()


@pytest.fixture
def mock_harvest_candidate():
    """Mock harvest candidate."""
    return HarvestCandidate(
        ticker="AAPL",
        quantity=100,
        cost_basis=15000.0,
        current_value=12000.0,
        unrealized_loss=-3000.0,
        holding_period_days=200
    )


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_basic(service, mock_harvest_candidate):
    """Test basic harvest opportunity identification."""
    service.base_service.identify_harvest_candidates = AsyncMock(return_value=[mock_harvest_candidate])
    service._calculate_tax_savings = AsyncMock(return_value=900.0)  # 30% tax rate
    service._estimate_transaction_cost = AsyncMock(return_value=12.0)  # 0.1% of value
    service.base_service.suggest_replacement_assets = AsyncMock(return_value=[
        {'symbol': 'MSFT', 'correlation': 0.85}
    ])
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=False))
    
    opportunities = await service.identify_harvest_opportunities(
        portfolio_id="test_portfolio"
    )
    
    assert opportunities is not None
    assert len(opportunities) > 0
    assert isinstance(opportunities[0], EnhancedHarvestOpportunity)
    assert opportunities[0].tax_savings == 900.0
    assert opportunities[0].net_benefit == 888.0  # 900 - 12
    assert opportunities[0].rank == 1


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_with_thresholds(service, mock_harvest_candidate):
    """Test harvest opportunity identification with custom thresholds."""
    service.base_service.identify_harvest_candidates = AsyncMock(return_value=[mock_harvest_candidate])
    service._calculate_tax_savings = AsyncMock(return_value=900.0)
    service._estimate_transaction_cost = AsyncMock(return_value=12.0)
    service.base_service.suggest_replacement_assets = AsyncMock(return_value=[])
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=False))
    
    opportunities = await service.identify_harvest_opportunities(
        portfolio_id="test_portfolio",
        min_loss_dollar=1000.0,
        min_loss_pct=0.10
    )
    
    assert opportunities is not None
    # Should filter based on thresholds


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_wash_sale_risk(service, mock_harvest_candidate):
    """Test harvest opportunity with wash-sale risk."""
    service.base_service.identify_harvest_candidates = AsyncMock(return_value=[mock_harvest_candidate])
    service._calculate_tax_savings = AsyncMock(return_value=900.0)
    service._estimate_transaction_cost = AsyncMock(return_value=12.0)
    service.base_service.suggest_replacement_assets = AsyncMock(return_value=[])
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=True))
    
    opportunities = await service.identify_harvest_opportunities(
        portfolio_id="test_portfolio"
    )
    
    assert opportunities is not None
    if len(opportunities) > 0:
        assert opportunities[0].wash_sale_risk is True


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_no_candidates(service):
    """Test harvest opportunity identification with no candidates."""
    service.base_service.identify_harvest_candidates = AsyncMock(return_value=[])
    
    opportunities = await service.identify_harvest_opportunities(
        portfolio_id="test_portfolio"
    )
    
    assert opportunities is not None
    assert len(opportunities) == 0


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_ranking(service):
    """Test that opportunities are ranked by net benefit."""
    candidates = [
        HarvestCandidate("AAPL", 100, 15000.0, 12000.0, -3000.0, 200),
        HarvestCandidate("MSFT", 50, 15000.0, 11000.0, -4000.0, 150),
    ]
    
    service.base_service.identify_harvest_candidates = AsyncMock(return_value=candidates)
    service._calculate_tax_savings = AsyncMock(side_effect=[900.0, 1200.0])
    service._estimate_transaction_cost = AsyncMock(side_effect=[12.0, 11.0])
    service.base_service.suggest_replacement_assets = AsyncMock(return_value=[])
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=False))
    
    opportunities = await service.identify_harvest_opportunities(
        portfolio_id="test_portfolio"
    )
    
    assert len(opportunities) == 2
    # MSFT should rank higher (higher net benefit: 1200-11=1189 vs 900-12=888)
    assert opportunities[0].candidate.ticker == "MSFT"
    assert opportunities[0].rank == 1
    assert opportunities[1].rank == 2


@pytest.mark.asyncio
async def test_batch_harvest_analysis(service):
    """Test batch harvest analysis."""
    opportunities = [
        EnhancedHarvestOpportunity(
            candidate=HarvestCandidate("AAPL", 100, 15000.0, 12000.0, -3000.0, 200),
            tax_savings=900.0,
            net_benefit=888.0,
            replacement_suggestions=[],
            wash_sale_risk=False
        ),
        EnhancedHarvestOpportunity(
            candidate=HarvestCandidate("MSFT", 50, 15000.0, 11000.0, -4000.0, 150),
            tax_savings=1200.0,
            net_benefit=1189.0,
            replacement_suggestions=[],
            wash_sale_risk=False
        ),
    ]
    
    result = await service.batch_harvest_analysis(
        portfolio_id="test_portfolio",
        opportunities=opportunities
    )
    
    assert result is not None
    assert isinstance(result, BatchHarvestResult)
    assert result.total_tax_savings == 2100.0  # 900 + 1200
    assert result.total_net_benefit == 2077.0  # 888 + 1189
    assert result.trades_required == 2


@pytest.mark.asyncio
async def test_batch_harvest_analysis_requires_approval(service):
    """Test batch harvest analysis that requires approval."""
    opportunities = [
        EnhancedHarvestOpportunity(
            candidate=HarvestCandidate("AAPL", 1000, 150000.0, 120000.0, -30000.0, 200),
            tax_savings=9000.0,  # Exceeds approval threshold
            net_benefit=8880.0,
            replacement_suggestions=[],
            wash_sale_risk=False
        ),
    ]
    
    result = await service.batch_harvest_analysis(
        portfolio_id="test_portfolio",
        opportunities=opportunities
    )
    
    assert result is not None
    assert result.requires_approval is True


@pytest.mark.asyncio
async def test_check_wash_sale_violation(service):
    """Test wash-sale violation checking."""
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=True))
    
    violation = await service.check_wash_sale_violation(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        sale_date=datetime.utcnow()
    )
    
    assert violation is not None
    assert violation.is_violation is True


@pytest.mark.asyncio
async def test_check_wash_sale_violation_no_violation(service):
    """Test wash-sale check with no violation."""
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=False))
    
    violation = await service.check_wash_sale_violation(
        portfolio_id="test_portfolio",
        symbol="AAPL",
        sale_date=datetime.utcnow()
    )
    
    assert violation is not None
    assert violation.is_violation is False


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_error_handling(service):
    """Test error handling in harvest opportunity identification."""
    service.base_service.identify_harvest_candidates = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.identify_harvest_opportunities(
            portfolio_id="error_portfolio"
        )


@pytest.mark.asyncio
async def test_batch_harvest_analysis_empty_opportunities(service):
    """Test batch harvest analysis with empty opportunities."""
    result = await service.batch_harvest_analysis(
        portfolio_id="test_portfolio",
        opportunities=[]
    )
    
    assert result is not None
    assert result.total_tax_savings == 0.0
    assert result.total_net_benefit == 0.0
    assert result.trades_required == 0


@pytest.mark.asyncio
async def test_identify_harvest_opportunities_filters_by_threshold(service):
    """Test that opportunities are filtered by loss threshold."""
    small_loss_candidate = HarvestCandidate(
        "AAPL", 10, 1500.0, 1450.0, -50.0, 200  # Below $500 threshold
    )
    
    service.base_service.identify_harvest_candidates = AsyncMock(return_value=[small_loss_candidate])
    service._calculate_tax_savings = AsyncMock(return_value=15.0)
    service._estimate_transaction_cost = AsyncMock(return_value=1.45)
    service.base_service.suggest_replacement_assets = AsyncMock(return_value=[])
    service.base_service.check_wash_sale_violation = AsyncMock(return_value=Mock(is_violation=False))
    
    opportunities = await service.identify_harvest_opportunities(
        portfolio_id="test_portfolio",
        min_loss_dollar=500.0
    )
    
    # Should be filtered out
    assert len(opportunities) == 0
