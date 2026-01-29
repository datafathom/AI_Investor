import pytest
from services.finance.op_cost_calculator import OperationalCostCalculator

def test_tco_calculation_active():
    svc = OperationalCostCalculator()
    # 1% fee, 0.2% spread, 0.5% tax drag, 0.1% cash drag -> 1.8% TCO
    res = svc.calculate_tco("ACTIVE_ALPHA", 0.01, 0.002, 0.005, 0.001)
    assert res == 0.018

def test_efficiency_gap_vs_beta():
    svc = OperationalCostCalculator()
    tco = 0.018
    # vs 0.03% beta -> 1.77% gap
    assert svc.compare_to_beta(tco, 0.0003) == 0.0177
