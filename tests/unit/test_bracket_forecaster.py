import pytest
from services.tax.bracket_forecaster import TaxBracketForecaster
from schemas.ira_optimization import IRAOptimizationProfile
from uuid import uuid4

def test_sunset_prediction():
    forecaster = TaxBracketForecaster()
    profile = IRAOptimizationProfile(
        user_id=uuid4(),
        current_marginal_rate=0.22,
        current_age=30,
        retirement_age=65,
        filing_status="SINGLE",
        current_agi=150000,
        projected_retirement_income=250000 # High income in retirement
    )
    rate = forecaster.forecast_retirement_bracket(profile)
    # Base rate (0.35) + Sunset Penalty (0.03) = 0.38
    assert rate == 0.38
