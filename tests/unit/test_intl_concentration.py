import pytest
from services.international.concentration_analyzer import IntlConcentrationAnalyzer

def test_skew_detection_tsmc():
    svc = IntlConcentrationAnalyzer()
    holdings = [
        {"ticker": "2330.TW", "weight": 0.31}, # TSMC in Taiwan index
        {"ticker": "2454.TW", "weight": 0.05}
    ]
    res = svc.analyze_index_skew("MSCI Taiwan", holdings)
    assert res["is_skewed"] == True
    assert res["top_ticker"] == "2330.TW"

def test_balanced_index():
    svc = IntlConcentrationAnalyzer()
    holdings = [
        {"ticker": "AAPL", "weight": 0.07},
        {"ticker": "MSFT", "weight": 0.06}
    ]
    res = svc.analyze_index_skew("S&P 500", holdings)
    assert res["is_skewed"] == False
