import pytest
from decimal import Decimal
from services.pe.waterfall_engine import WaterfallEngine
from services.lending.stock_lending_svc import StockLendingService

@pytest.fixture
def waterfall():
    return WaterfallEngine()

@pytest.fixture
def lending():
    return StockLendingService()

def test_waterfall_basic_dist(waterfall):
    # $1M invest, 8% pref, $100k cash. LP gets $80k pref + 80% of $20k = $96k. GP gets 20% of 20k = $4k.
    result = waterfall.calculate_distributions(Decimal('100000'), Decimal('1000000'))
    assert result['total_lp_dist'] == Decimal('96000.00')
    assert result['total_gp_dist'] == Decimal('4000.00')

def test_stock_borrowing_capacity_low_vol(lending):
    # $1B position, 15% vol -> 50% LTV ($500M)
    result = lending.calculate_borrowing_power("AAPL", Decimal('1000000000'), 15.0)
    assert result['available_liquidity'] == Decimal('500000000.00')
    assert result['max_ltv'] == Decimal('0.50')

def test_borrow_vs_sell_recommendation(lending):
    # $1M value, $0 basis, 20% cap gains = $200k tax.
    # Interest at 5% on $500k loan = $25k/yr.
    # Breakeven = 8 years. Recommend BORROW.
    result = lending.analyze_borrow_vs_sell(Decimal('1000000'), Decimal('0'), Decimal('0.20'), Decimal('0.05'))
    assert result['recommendation'] == "BORROW"
    assert result['breakeven_years'] == 8.0
