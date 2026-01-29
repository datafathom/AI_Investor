import pytest
from services.reits.property_classifier import PropertyClassifier

def test_reit_classification():
    svc = PropertyClassifier()
    assert svc.classify_ticker("O") == "RETAIL"
    assert svc.classify_ticker("DLR") == "DATA_CENTER"
    assert svc.classify_ticker("FAKE") == "DIVERSIFIED"

def test_inflation_hedge_scores():
    svc = PropertyClassifier()
    assert svc.evaluate_inflation_hedge("AGRICULTURE") == 0.95
    assert svc.evaluate_inflation_hedge("OFFICE") == 0.30
