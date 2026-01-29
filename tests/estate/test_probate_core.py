import pytest
from decimal import Decimal
from services.estate.probate_fee_calc import ProbateFeeCalculator
from services.legal.intestacy_logic import IntestacyLogic

@pytest.fixture
def fee_calc():
    return ProbateFeeCalculator()

@pytest.fixture
def intestacy():
    return IntestacyLogic()

def test_probate_fee_calculation_ca(fee_calc):
    # $1.5M estate
    # 4% of 100k = 4k
    # 3% of 100k = 3k
    # 2% of 800k = 16k
    # 1% of 500k = 5k
    # Total statutory fee = 28k (for one party)
    # total_statutory_fees (both) = 56k
    result = fee_calc.calculate_statutory_fees(Decimal('1500000'))
    assert result['attorney_fee'] == Decimal('28000.00')
    assert result['total_statutory_fees'] == Decimal('56000.00')

def test_intestacy_logic_spouse_only(intestacy):
    result = intestacy.identify_legal_heirs(True, 0, 1000000)
    assert len(result) == 1
    assert result[0]['heir'] == "SPOUSE"
    assert result[0]['share_pct'] == 100.0

def test_intestacy_logic_spouse_and_child(intestacy):
    result = intestacy.identify_legal_heirs(True, 1, 1000000)
    assert len(result) == 2
    assert result[0]['share_pct'] == 50.0
    assert result[1]['share_pct'] == 50.0
