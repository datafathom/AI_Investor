import pytest
from config.environment_manager import get_settings
from services.analysis.macro_service import MacroService
from services.analysis.esg_service import ESGService
from services.trading.corporate_service import CorporateService
from services.philanthropy.donation_service import DonationService
from services.portfolio_manager import PortfolioManager, PortfolioType, Position, ConvictionLevel

@pytest.fixture
def mock_pm():
    pm = PortfolioManager(total_capital=1000000.0)
    pm.add_position(PortfolioType.AGGRESSIVE, "TSLA", 10, 200.0, ConvictionLevel.HIGH)
    pm.add_position(PortfolioType.DEFENSIVE, "AAPL", 100, 180.0)
    return pm

@pytest.mark.asyncio
async def test_macro_service_fred_integration():
    service = MacroService()
    # Even in mock mode, it should return formatted data
    cpi = await service.get_regional_cpi("USA")
    assert cpi.country_code == "USA"
    assert cpi.current_cpi > 0
    
    map_data = await service.get_world_map_data()
    assert "USA" in map_data
    assert "unemployment" in map_data["USA"]

@pytest.mark.asyncio
async def test_esg_service_dynamic_scoring(mock_pm):
    service = ESGService()
    tickers = [p.symbol for p in mock_pm.defensive.positions]
    tickers += [p.symbol for p in mock_pm.aggressive.positions]
    
    score = await service.get_portfolio_esg_scores(tickers)
    # TSLA (90) + AAPL (75) -> ~82.5
    assert score.composite > 70
    assert score.grade in ["A", "B"]

@pytest.mark.asyncio
async def test_corporate_service_fallback():
    service = CorporateService()
    # Should at least return mock data if AV key is missing/invalid
    earnings = await service.get_earnings_calendar(30)
    assert len(earnings) > 0
    assert earnings[0].ticker in ["TSLA", "AAPL", "MSFT"] or earnings[0].ticker is not None

@pytest.mark.asyncio
async def test_givingblock_prod_check():
    from services.philanthropy.charity_client import GivingBlockClient
    from config.environment_manager import get_settings
    
    settings = get_settings()
    # Force production env for test
    client = GivingBlockClient()
    client.env = "production"
    client.api_key = "mock_key_123"
    
    with pytest.raises(ValueError, match="GivingBlock API Key is required"):
        await client.create_donation_transaction(100.0, "Climate")
