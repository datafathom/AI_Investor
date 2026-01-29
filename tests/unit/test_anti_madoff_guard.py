import pytest
from services.fraud.anti_madoff_guard import AntiMadoffGuard

def test_madoff_pattern_detection():
    guard = AntiMadoffGuard()
    # Very consistent monthly returns (exactly 0.8% every month)
    fake_returns = [0.008 for _ in range(12)]
    assert guard.detect_return_striation(fake_returns) == True

def test_normal_returns():
    guard = AntiMadoffGuard()
    # Volatile returns
    real_returns = [0.01, -0.02, 0.05, 0.001, -0.01, 0.02, 0.03, -0.04, 0.01, 0.02, -0.01, 0.05]
    assert guard.detect_return_striation(real_returns) == False

def test_source_verification():
    guard = AntiMadoffGuard()
    assert guard.validate_statement_source("SCHWAB", "SCHWAB") == True
    assert guard.validate_statement_source("ADVISOR_INC", "SCHWAB") == False
