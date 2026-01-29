import pytest
from decimal import Decimal
from services.simulation.geopolitical_sim_engine import GeopoliticalSimEngine
from services.legal.citizenship_hedging_svc import CitizenshipHedgingService
from services.quantitative.liquidity_alpha_svc import LiquidityAlphaService

@pytest.fixture
def geo_sim():
    return GeopoliticalSimEngine()

@pytest.fixture
def citizen_svc():
    return CitizenshipHedgingService()

@pytest.fixture
def liq_svc():
    return LiquidityAlphaService()

def test_geopolitical_impact_calc(geo_sim):
    # 50% tech, 50% defense
    # Tech shock -0.4, Defense shock +0.2 -> Net -0.1 (-10%)
    exposures = {"TECH": 0.5, "DEFENSE": 0.5}
    result = geo_sim.simulate_tail_risk("Conflict", exposures)
    assert result['projected_portfolio_delta_pct'] == -10.0

def test_residency_cushion_risk(citizen_svc):
    # 170 days spent -> 13 remaining -> RISK
    result = citizen_svc.track_residency_threshold("PT", 170)
    assert result['status'] == "RISK_OF_TAX_RECOGNITION"
    assert result['days_remaining_to_resident'] == 13

def test_risk_parity_selling_pressure(liq_svc):
    # 10% vol increase on $10B AUM -> $0.5B sell
    result = liq_svc.predict_risk_parity_flow(10.0, 10.0)
    assert result['est_market_sell_pressure_bn'] == 0.5
