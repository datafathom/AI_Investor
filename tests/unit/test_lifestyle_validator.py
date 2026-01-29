import pytest
from services.planning.lifestyle_validator import LifestyleValidator

def test_lifestyle_maintained():
    svc = LifestyleValidator()
    # 7% return, 3% inflation -> Positive real growth
    res = svc.validate_purchasing_power(1000000, 10, 0.03, 0.07)
    assert res["is_maintained"] == True
    assert res["status"] == "MAINTAINED"

def test_lifestyle_declining():
    svc = LifestyleValidator()
    # 2% return, 5% inflation -> Negative real growth
    res = svc.validate_purchasing_power(1000000, 10, 0.05, 0.02)
    assert res["is_maintained"] == False
    assert res["status"] == "DECLINING"
