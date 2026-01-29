import pytest
from services.analysis.farmland_hedge import FarmlandHedgeEvaluator

def test_farmland_beta():
    svc = FarmlandHedgeEvaluator()
    # 8% land price increase, 4% food inflation -> Beta 2.0
    assert svc.evaluate_food_inflation_beta(0.08, 0.04) == 2.0

def test_water_risk_detection():
    svc = FarmlandHedgeEvaluator()
    assert svc.assess_risk(False, "CALIFORNIA") == "HIGH_RISK_WATER_SCARCITY"
    assert svc.assess_risk(True, "IOWA") == "STABLE"
