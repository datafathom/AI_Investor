import pytest
from decimal import Decimal
from services.credit.credit_risk_engine import CreditRiskEngine
from services.private_markets.premium_optimizer import PremiumOptimizer

@pytest.fixture
def risk_engine():
    return CreditRiskEngine()

@pytest.fixture
def optimizer():
    return PremiumOptimizer()

def test_calculate_net_yield_stable(risk_engine):
    # 5% base + 600bps spread = 11%. 1% prob, 90% recovery = 0.1% loss. Net = 10.9%
    result = risk_engine.calculate_expected_net_yield(
        600, Decimal('0.05'), Decimal('0.01'), Decimal('0.90')
    )
    assert result['net_yield_pct'] == Decimal('10.90')
    assert result['risk_status'] == "STABLE"

def test_illiquidity_premium_check(optimizer):
    # 15% private vs 10% public = 500bps premium
    result = optimizer.calculate_illiquidity_premium(Decimal('0.15'), Decimal('0.10'))
    assert result['premium_bps'] == 500
    assert result['is_sufficient'] is True

def test_return_unsmoothing_geltner(optimizer):
    # Smoothed returns for 3 quarters. Rho=0.5
    smoothed = [0.02, 0.04, 0.01]
    # R2_true = (0.04 - 0.5*0.02) / 0.5 = 0.03/0.5 = 0.06
    unsmoothed = optimizer.unsmooth_returns(smoothed, rho=0.5)
    assert unsmoothed[1] == 0.06
