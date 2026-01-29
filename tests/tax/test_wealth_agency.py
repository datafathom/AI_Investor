import pytest
from decimal import Decimal
from services.tax.wealth_tax_engine import WealthTaxEngine
from services.performance.active_share_svc import ActiveShareService

@pytest.fixture
def tax_engine():
    return WealthTaxEngine()

@pytest.fixture
def active_share_svc():
    return ActiveShareService()

def test_wealth_tax_spiral_calc(tax_engine):
    # $1M bill with 20% CGT rate -> requires $1.25M sale
    # Math: 1,000,000 / (1 - 0.2) = 1,250,000
    result = tax_engine.simulate_tax_on_tax_spiral(Decimal('1000000'), Decimal('0.20'))
    assert result['total_liquidity_needed'] == Decimal('1250000.00')
    assert result['liquidation_triggered_cgt'] == Decimal('250000.00')

def test_active_share_herding_detection(active_share_svc):
    # Portfolio: 100% AAPL. Bench: 50% AAPL, 50% MSFT.
    # Diff: |1.0 - 0.5| + |0.0 - 0.5| = 0.5 + 0.5 = 1.0.
    # Active Share = 0.5 * 1.0 = 0.5 (Herding/Closet Index)
    port = {"AAPL": Decimal('1.0')}
    bench = {"AAPL": Decimal('0.5'), "MSFT": Decimal('0.5')}
    res = active_share_svc.calculate_active_share(port, bench)
    assert res == 0.5
