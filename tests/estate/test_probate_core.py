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
    assert result['attorney_statutory_fee'] == 28000.0
    assert result['total_statutory_cost'] == 56000.0

def test_intestacy_logic_spouse_only(intestacy):
    # Spouse, 0 kids, No parents, 1M community, 0 separate
    result = intestacy.map_succession(True, 0, False, 1000000.0, 0.0)
    distributions = [d for d in result['distributions'] if d['value'] > 0]
    assert len(distributions) == 1
    assert distributions[0]['party'] == "Spouse"
    assert distributions[0]['value'] == 1000000.0

def test_intestacy_logic_spouse_and_child(intestacy):
    # Spouse, 1 kid, No parents, 0 community, 1M separate -> 50/50 split
    result = intestacy.map_succession(True, 1, False, 0.0, 1000000.0)
    distributions = [d for d in result['distributions'] if d['value'] > 0]
    assert len(distributions) == 2
    # Order: Spouse, Child 1
    assert distributions[0]['party'] == "Spouse"
    assert distributions[0]['value'] == 500000.0
    assert distributions[1]['party'] == "Child 1"
    assert distributions[1]['value'] == 500000.0
