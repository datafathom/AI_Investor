import pytest
import datetime
from services.analysis.macro_service import MacroService

class TestMacroService:
    
    @pytest.mark.asyncio
    async def test_political_insider_trades(self):
        service = MacroService()
        
        # Test basic fetch
        trades = await service.get_political_insider_trades()
        assert len(trades) > 0
        assert trades[0].country in ["USA", "UK"]
        
        # Test region filter (US)
        us_trades = await service.get_political_insider_trades("USA")
        for trade in us_trades:
            assert trade.country == "USA"
            
        # Test region filter (Europe)
        eu_trades = await service.get_political_insider_trades("Europe")
        for trade in eu_trades:
            assert trade.country in ["UK", "Germany", "France"]

    @pytest.mark.asyncio
    async def test_regional_cpi(self):
        service = MacroService()
        
        # Test known country
        us_cpi = await service.get_regional_cpi("USA")
        assert us_cpi.current_cpi > 0
        assert us_cpi.yoy_change is not None
        
        # Test unknown country fallback
        unknown_cpi = await service.get_regional_cpi("MARS")
        assert unknown_cpi.country_name == "MARS"
        assert unknown_cpi.current_cpi == 100.0

    @pytest.mark.asyncio
    async def test_inflation_hedge_correlations(self):
        service = MacroService()
        
        matrix = await service.get_inflation_hedge_correlations()
        assert "GLD" in matrix.assets
        assert "TIP" in matrix.assets
        # Gold should correlate with CPI
        assert matrix.correlations["GLD"]["CPI"] > 0
