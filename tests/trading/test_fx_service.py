"""
Test FX Service - Phase 56 Unit Tests

Tests for foreign exchange rates, currency conversion,
and cash optimization features.

Run with:
    .\\venv\\Scripts\\python.exe -m pytest tests/trading/test_fx_service.py -v
"""

import pytest
from services.trading.fx_service import (
    FXService,
    FXRate,
    CurrencyBalance,
    SweepSuggestion,
    RepoRate,
    ConversionResult,
    get_fx_service
)


@pytest.fixture
def fx_service() -> FXService:
    """Create FX service instance."""
    return FXService()


class TestFXRates:
    """Tests for FX rate functionality."""
    
    @pytest.mark.asyncio
    async def test_get_fx_rates(self, fx_service: FXService) -> None:
        """Test getting FX rates."""
        rates = await fx_service.get_fx_rates()
        
        assert isinstance(rates, list)
        assert len(rates) >= 5
        
        for rate in rates:
            assert isinstance(rate, FXRate)
            assert rate.pair
            assert rate.rate > 0
            assert rate.bid > 0
            assert rate.ask > 0
            assert rate.ask >= rate.bid
    
    @pytest.mark.asyncio
    async def test_fx_rates_have_spread(self, fx_service: FXService) -> None:
        """Test that FX rates have bid/ask spread."""
        rates = await fx_service.get_fx_rates()
        
        for rate in rates:
            assert rate.spread_bps >= 0
            calculated_spread = ((rate.ask - rate.bid) / rate.bid) * 10000
            # Allow some tolerance
            assert abs(calculated_spread - rate.spread_bps) < 1.0
    
    @pytest.mark.asyncio
    async def test_major_pairs_available(self, fx_service: FXService) -> None:
        """Test that major currency pairs are available."""
        rates = await fx_service.get_fx_rates()
        pairs = [r.pair for r in rates]
        
        assert "EUR/USD" in pairs
        assert "GBP/USD" in pairs
        assert "USD/JPY" in pairs


class TestCurrencyBalances:
    """Tests for currency balance functionality."""
    
    @pytest.mark.asyncio
    async def test_get_balances(self, fx_service: FXService) -> None:
        """Test getting currency balances."""
        balances = await fx_service.get_balances()
        
        assert isinstance(balances, list)
        assert len(balances) >= 1
        
        for balance in balances:
            assert isinstance(balance, CurrencyBalance)
            assert balance.currency
            assert balance.amount >= 0
            assert balance.amount_usd >= 0
    
    @pytest.mark.asyncio
    async def test_total_value_usd(self, fx_service: FXService) -> None:
        """Test total value calculation."""
        total = await fx_service.get_total_value_usd()
        balances = await fx_service.get_balances()
        
        calculated_total = sum(b.amount_usd for b in balances)
        assert abs(total - calculated_total) < 0.01
    
    @pytest.mark.asyncio
    async def test_usd_balance_exists(self, fx_service: FXService) -> None:
        """Test that USD balance exists with interest rate."""
        balances = await fx_service.get_balances()
        
        usd = next((b for b in balances if b.currency == "USD"), None)
        assert usd is not None
        assert usd.interest_rate > 0


class TestFXConversion:
    """Tests for FX conversion functionality."""
    
    @pytest.mark.asyncio
    async def test_execute_conversion(self, fx_service: FXService) -> None:
        """Test basic FX conversion."""
        result = await fx_service.execute_conversion("USD", "EUR", 1000)
        
        assert isinstance(result, ConversionResult)
        assert result.from_currency == "USD"
        assert result.to_currency == "EUR"
        assert result.from_amount == 1000
        assert result.to_amount > 0
        assert result.rate_used > 0
    
    @pytest.mark.asyncio
    async def test_conversion_rate_reasonable(self, fx_service: FXService) -> None:
        """Test that conversion rates are reasonable."""
        result = await fx_service.execute_conversion("USD", "EUR", 1000)
        
        # EUR/USD typically 0.85-1.15
        assert 0.5 < result.rate_used < 2.0
    
    @pytest.mark.asyncio
    async def test_conversion_updates_balances(self, fx_service: FXService) -> None:
        """Test that conversion updates balances."""
        initial_balances = await fx_service.get_balances()
        initial_usd = next((b.amount for b in initial_balances if b.currency == "USD"), 0)
        
        await fx_service.execute_conversion("USD", "EUR", 1000)
        
        updated_balances = await fx_service.get_balances()
        updated_usd = next((b.amount for b in updated_balances if b.currency == "USD"), 0)
        
        assert updated_usd == initial_usd - 1000
    
    @pytest.mark.asyncio
    async def test_conversion_spread_cost(self, fx_service: FXService) -> None:
        """Test that spread cost is calculated."""
        result = await fx_service.execute_conversion("USD", "EUR", 10000)
        
        assert result.spread_cost >= 0


class TestSweepSuggestions:
    """Tests for cash sweep suggestions."""
    
    @pytest.mark.asyncio
    async def test_get_sweep_suggestions(self, fx_service: FXService) -> None:
        """Test getting sweep suggestions."""
        suggestions = await fx_service.get_sweep_suggestions()
        
        assert isinstance(suggestions, list)
        # Should have suggestions if USD balance > 50k
        assert len(suggestions) >= 1
    
    @pytest.mark.asyncio
    async def test_sweep_suggestion_fields(self, fx_service: FXService) -> None:
        """Test sweep suggestion fields."""
        suggestions = await fx_service.get_sweep_suggestions()
        
        for s in suggestions:
            assert isinstance(s, SweepSuggestion)
            assert s.id
            assert s.from_currency
            assert s.to_vehicle
            assert s.amount > 0
            assert s.projected_yield > 0
            assert s.risk in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_mmf_suggestion_present(self, fx_service: FXService) -> None:
        """Test that MMF suggestion is included."""
        suggestions = await fx_service.get_sweep_suggestions()
        
        vehicles = [s.to_vehicle for s in suggestions]
        assert any("MMF" in v for v in vehicles)


class TestRepoRates:
    """Tests for repo rate functionality."""
    
    @pytest.mark.asyncio
    async def test_get_repo_rates(self, fx_service: FXService) -> None:
        """Test getting repo rates."""
        rates = await fx_service.get_repo_rates()
        
        assert isinstance(rates, list)
        assert len(rates) >= 3
        
        for rate in rates:
            assert isinstance(rate, RepoRate)
            assert rate.region
            assert rate.name
            assert rate.rate >= 0
    
    @pytest.mark.asyncio
    async def test_fed_funds_rate_present(self, fx_service: FXService) -> None:
        """Test Fed Funds rate is included."""
        rates = await fx_service.get_repo_rates()
        
        names = [r.name for r in rates]
        assert "Fed Funds Rate" in names
    
    @pytest.mark.asyncio
    async def test_regional_rates(self, fx_service: FXService) -> None:
        """Test rates from multiple regions."""
        rates = await fx_service.get_repo_rates()
        
        regions = set(r.region for r in rates)
        assert "US" in regions
        assert "EU" in regions


class TestCarryTrade:
    """Tests for carry trade detection."""
    
    @pytest.mark.asyncio
    async def test_detect_carry_trade(self, fx_service: FXService) -> None:
        """Test carry trade detection."""
        opportunity = await fx_service.detect_carry_trade_opportunity()
        
        assert isinstance(opportunity, dict)
        assert "opportunity" in opportunity
    
    @pytest.mark.asyncio
    async def test_carry_trade_fields_when_opportunity(
        self,
        fx_service: FXService
    ) -> None:
        """Test carry trade fields when opportunity exists."""
        opportunity = await fx_service.detect_carry_trade_opportunity()
        
        if opportunity.get("opportunity"):
            assert "borrow_currency" in opportunity
            assert "invest_currency" in opportunity
            assert "spread_percent" in opportunity
            assert opportunity["spread_percent"] > 4.0


class TestExposureLimit:
    """Tests for currency exposure limits."""
    
    @pytest.mark.asyncio
    async def test_check_exposure_limit(self, fx_service: FXService) -> None:
        """Test exposure limit check."""
        # Small amount shouldn't exceed limit
        total = await fx_service.get_total_value_usd()
        small_amount = total * 0.05
        
        exceeded = await fx_service.check_exposure_limit("CHF", small_amount)
        assert exceeded is False
    
    @pytest.mark.asyncio
    async def test_large_exposure_exceeds_limit(self, fx_service: FXService) -> None:
        """Test that large exposure exceeds limit."""
        total = await fx_service.get_total_value_usd()
        large_amount = total * 0.5
        
        exceeded = await fx_service.check_exposure_limit("CHF", large_amount)
        assert exceeded is True


class TestSupportedCurrencies:
    """Tests for supported currencies."""
    
    def test_get_supported_currencies(self, fx_service: FXService) -> None:
        """Test getting supported currencies list."""
        currencies = fx_service.get_supported_currencies()
        
        assert isinstance(currencies, list)
        assert len(currencies) >= 6
        assert "USD" in currencies
        assert "EUR" in currencies
        assert "GBP" in currencies


class TestSingleton:
    """Tests for service singleton."""
    
    def test_get_fx_service_singleton(self) -> None:
        """Test singleton pattern."""
        service1 = get_fx_service()
        service2 = get_fx_service()
        
        assert service1 is service2
