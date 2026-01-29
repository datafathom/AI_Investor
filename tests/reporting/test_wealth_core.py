import pytest
from decimal import Decimal
from services.reporting.total_wealth import TotalWealthCalculator

@pytest.fixture
def calculator():
    return TotalWealthCalculator()

def test_aggregate_net_worth_qp(calculator):
    # $3M Liquid + $2M Trust + $1M PPLI + $1M Private = $7M (Qualified Purchaser)
    result = calculator.aggregate_net_worth(
        Decimal('3000000'), Decimal('2000000'), Decimal('1000000'), Decimal('1000000')
    )
    assert result['total_net_worth'] == Decimal('7000000.00')
    assert result['status'] == "QUALIFIED_PURCHASER"
    assert result['alternative_exposure_pct'] > 25.0

def test_aggregate_net_worth_retail(calculator):
    # $400k total
    result = calculator.aggregate_net_worth(
        Decimal('300000'), Decimal('0'), Decimal('100000'), Decimal('0')
    )
    assert result['total_net_worth'] == Decimal('400000.00')
    assert result['status'] == "RETAIL_WEALTH"
