import pytest
from services.planning.complexity_analyzer import ComplexityAnalyzer

def test_simple_complexity():
    analyzer = ComplexityAnalyzer()
    # Low NW, no extras
    score = analyzer.analyze_complexity({"net_worth": 100000})
    assert score == 0.1
    assert analyzer.requires_human(score) == False

def test_high_complexity():
    analyzer = ComplexityAnalyzer()
    # High NW + Business + International
    score = analyzer.analyze_complexity({
        "net_worth": 50000000, 
        "has_business": True,
        "international_assets": True
    })
    assert score == 1.0
    assert analyzer.requires_human(score) == True
