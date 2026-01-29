import pytest
from services.quantitative.rolling_correlation import RollingCorrelationEngine

def test_correlation_positive():
    svc = RollingCorrelationEngine()
    # Perfectly correlated
    a = [1, 2, 3, 4, 5]
    b = [10, 20, 30, 40, 50]
    assert svc.calculate_correlation(a, b) == 1.0

def test_correlation_negative():
    svc = RollingCorrelationEngine()
    # Inversely correlated
    a = [1, 2, 3, 4, 5]
    b = [5, 4, 3, 2, 1]
    assert svc.calculate_correlation(a, b) == -1.0

def test_crisis_spike_detection():
    svc = RollingCorrelationEngine()
    # Spike from 0.4 to 0.9
    assert svc.identify_crisis_spike(0.4, 0.9) == True
    # Normal fluctuation
    assert svc.identify_crisis_spike(0.4, 0.5) == False
