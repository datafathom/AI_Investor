import pytest
from decimal import Decimal
from services.billing.carry_calculator import CarryEngine

@pytest.fixture
def carry_engine():
    return CarryEngine()

def test_calculate_carry_accrued(carry_engine):
    # $1.2M current, $1M peak/opening, 5% hurdle, 20% carry
    # Target = 1.05M. Bass Alpha = 0.15M. Fee = 0.03M
    result = carry_engine.calculate_performance_fee(
        current_nav=Decimal('1200000'), 
        previous_peak_nav=Decimal('1000000'), 
        opening_nav=Decimal('1000000')
    )
    assert result['fee_amount'] == Decimal('30000.00')
    assert result['status'] == "ACCRUED"

def test_calculate_carry_hwm_failure(carry_engine):
    # Current $900k, Peak $1M -> No fee
    result = carry_engine.calculate_performance_fee(
        current_nav=Decimal('900000'), 
        previous_peak_nav=Decimal('1000000'), 
        opening_nav=Decimal('800000')
    )
    assert result['fee_amount'] == Decimal('0.00')
    assert result['reason'] == "BELOW_HIGH_WATER_MARK"
