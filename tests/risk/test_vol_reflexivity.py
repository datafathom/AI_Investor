import pytest
from decimal import Decimal
from services.risk.volatility_monitor import VolatilityMonitor
from services.quantitative.reflexivity_engine import ReflexivityEngine

@pytest.fixture
def vol_monitor():
    return VolatilityMonitor()

@pytest.fixture
def reflex_engine():
    return ReflexivityEngine()

def test_vol_valuation_gap_alert(vol_monitor):
    # Proxy down 20% (-0.20), Private down 2% (-0.02). Gap = -0.18
    result = vol_monitor.calculate_valuation_gap(Decimal('-0.02'), Decimal('-0.20'))
    assert result['valuation_gap_pct'] == Decimal('-18.00')
    assert result['markdown_recommendation'] == "REQUIRED"

def test_reflexivity_saturation_logic(reflex_engine):
    # Big Three own 500M / 1B shares = 50% -> SATURATED
    result = reflex_engine.check_passive_saturation("AAPL", 500000000, 1000000000)
    assert result['is_saturated_reflexive'] is True
    assert result['passive_ownership_pct'] == Decimal('50.00')

def test_inelastic_flow_impact(reflex_engine):
    # $100 price, 100M inflow, 0.2 coef -> 20% move -> $120
    new_price = reflex_engine.simulate_inelastic_flow_impact(100.0, 100.0, 0.2)
    assert new_price == 120.0
