import pytest
import asyncio
from services.risk.margin_service import MarginService, MarginStatus
from services.portfolio_manager import PortfolioManager, PortfolioType, Position, ConvictionLevel

@pytest.fixture
def mock_pm():
    pm = PortfolioManager(total_capital=1000000.0)
    # Add some mock positions
    pm.add_position(
        portfolio_type=PortfolioType.AGGRESSIVE,
        symbol="TSLA",
        quantity=100,
        price=200.0,
        conviction=ConvictionLevel.HIGH,
        leverage=2.0
    )
    pm.add_position(
        portfolio_type=PortfolioType.DEFENSIVE,
        symbol="SPY",
        quantity=500,
        price=400.0
    )
    return pm

@pytest.mark.asyncio
async def test_margin_buffer_calculation(mock_pm):
    service = MarginService(portfolio_manager=mock_pm)
    buffer = await service.calculate_margin_buffer()
    
    # Equity = (100*200 + 500*400 + Cash) - MarginUsed
    # Initial Cash = 1,000,000
    # TSLA Cost = 20,000. SPY Cost = 200,000.
    # Total Value = 1,000,000. Margin Used = 450,000 (default in service)
    # Equity = 1,000,000 - 450,000 = 550,000
    
    # Maint Req: 
    # TSLA (Aggressive & Leveraged 2x): 20,000 * 0.30 * 2.0 = 12,000
    # SPY (Defensive): 200,000 * 0.15 = 30,000
    # Total Maint = 42,000
    
    # Buffer = (550,000 - 42,000) / 550,000 * 100 = 508,000 / 550,000 * 100 = ~92.36%
    
    assert buffer > 90
    assert buffer < 95

@pytest.mark.asyncio
async def test_deleverage_plan_generation(mock_pm):
    service = MarginService(portfolio_manager=mock_pm)
    
    # Force a deleverage by requesting a high buffer
    plan = await service.generate_deleverage_plan(target_buffer=95)
    
    assert plan.total_to_sell > 0
    assert len(plan.positions_to_close) > 0
    assert plan.positions_to_close[0]['ticker'] == "TSLA" # Aggressive sold first
    assert plan.urgency == "low" # Buffer is still high

@pytest.mark.asyncio
async def test_danger_zone(mock_pm):
    service = MarginService(portfolio_manager=mock_pm)
    # Low margin used, so buffer is high
    is_danger = await service.check_danger_zone()
    assert is_danger is False
    
    # Artificially increase margin used to trigger danger
    service._margin_used = 900000 
    # Equity = 1M - 900K = 100K
    # Maint Req = 42K
    # Buffer = (100 - 42) / 100 * 100 = 58% -> Wait, 58 is still > 20.
    
    service._margin_used = 955000
    # Equity = 1M - 955K = 45K
    # Maint Req = 42K
    # Buffer = (45 - 42) / 45 * 100 = 3 / 45 * 100 = 6.6%
    
    is_danger = await service.check_danger_zone()
    assert is_danger is True
