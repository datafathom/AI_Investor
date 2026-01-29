import pytest
from services.analysis.fundamental_distortion import FundamentalDistortionLogger

def test_distortion_score():
    svc = FundamentalDistortionLogger()
    # 10% cap weight, 5% revenue weight -> 2.0 Distortion
    assert svc.calculate_distortion(0.10, 0.05) == 2.0
    assert svc.classify_distortion(2.1) == "SEVERE"

def test_minimal_distortion():
    svc = FundamentalDistortionLogger()
    # 10% cap weight, 9.5% rev weight -> ~1.05
    res = svc.calculate_distortion(0.10, 0.095)
    assert svc.classify_distortion(res) == "MINOR"
