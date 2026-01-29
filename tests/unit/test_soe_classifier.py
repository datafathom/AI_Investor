import pytest
from services.international.soe_classifier import SOEClassifier

def test_soe_classification_ownership():
    svc = SOEClassifier()
    # 51% owned -> SOE
    assert svc.classify_soe(0.51, "General Public") == True
    # 20% owned -> Not SOE
    assert svc.classify_soe(0.20, "General Public") == False

def test_soe_classification_entity():
    svc = SOEClassifier()
    # SASAC (China) control -> SOE regardless of specific %
    assert svc.classify_soe(0.1, "SASAC") == True

def test_risk_rating():
    svc = SOEClassifier()
    # Chinese SOE -> Critical
    assert svc.get_risk_rating(True, "CN") == "CRITICAL"
    # Swiss SOE -> High
    assert svc.get_risk_rating(True, "CH") == "HIGH"
    # Swiss private -> Low
    assert svc.get_risk_rating(False, "CH") == "LOW"
