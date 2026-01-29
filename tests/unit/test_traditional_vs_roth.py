import pytest
from services.tax.traditional_vs_roth import TraditionalVsRothAnalyzer
from models.ira_optimization import IRAOptimizationProfile
from uuid import uuid4

def test_roth_better_at_low_age():
    analyzer = TraditionalVsRothAnalyzer()
    profile = IRAOptimizationProfile(
        user_id=uuid4(),
        current_marginal_rate=0.22,
        projected_retirement_rate=0.35, # Expect higher in future
        current_age=25,
        retirement_age=65,
        filing_status="SINGLE",
        current_agi=100000
    )
    result = analyzer.analyze(profile)
    assert result.recommendation == "ROTH"

def test_traditional_better_at_high_rate():
    analyzer = TraditionalVsRothAnalyzer()
    profile = IRAOptimizationProfile(
        user_id=uuid4(),
        current_marginal_rate=0.37, # High current rate
        projected_retirement_rate=0.20, # Low future rate
        current_age=55,
        retirement_age=65,
        filing_status="SINGLE",
        current_agi=600000
    )
    result = analyzer.analyze(profile)
    assert result.recommendation == "TRADITIONAL"
