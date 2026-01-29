import pytest
from services.planning.career_risk_scorer import CareerRiskScorer

def test_career_risk_calculation():
    scorer = CareerRiskScorer()
    # High risk data
    data = {
        "industry_volatility": 0.9,
        "income_stability": 0.1,
        "job_market_health": 0.2
    }
    multiplier = scorer.calculate_risk_factor(data)
    assert multiplier > 1.5

def test_career_risk_safe():
    scorer = CareerRiskScorer()
    # Safe data
    data = {
        "industry_volatility": 0.1,
        "income_stability": 0.9,
        "job_market_health": 0.9
    }
    multiplier = scorer.calculate_risk_factor(data)
    assert multiplier < 1.3
