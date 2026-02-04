import pytest
from services.planning.spending_analyzer import SpendingAnalyzer
from schemas.spending import SpendingCategory
from uuid import uuid4
from datetime import date

def test_spending_analysis_waste():
    analyzer = SpendingAnalyzer()
    spending = SpendingCategory(
        user_id=uuid4(),
        month=date(2026, 1, 1),
        subscriptions=300.0, # High
        food_dining=1200.0,  # High
        housing=3000.0,
        savings_contributions=1000.0
    )
    res = analyzer.analyze_patterns(spending)
    assert len(res["opportunities"]) == 2
    assert res["savings_rate"] > 0

def test_spending_analysis_lean():
    analyzer = SpendingAnalyzer()
    spending = SpendingCategory(
        user_id=uuid4(),
        month=date(2026, 1, 1),
        subscriptions=50.0,
        food_dining=400.0,
        housing=2000.0,
        savings_contributions=2000.0
    )
    res = analyzer.analyze_patterns(spending)
    assert len(res["opportunities"]) == 0
    assert res["savings_rate"] > 0.4
