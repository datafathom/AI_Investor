import pytest
from decimal import Decimal
from services.sfo.sfo_justification import SFOJustificationEngine
from services.mfo.expense_allocator import MFOExpenseAllocator

@pytest.fixture
def sfo_engine():
    return SFOJustificationEngine()

@pytest.fixture
def mfo_allocator():
    return MFOExpenseAllocator()

def test_sfo_breakeven_large_estate(sfo_engine):
    # $500M AUM at 1% fee is $5M. SFO costs ~$1M.
    result = sfo_engine.run_breakeven_analysis(Decimal('500000000'))
    assert result['is_sfo_economically_viable'] is True
    assert result['annual_savings'] > Decimal('3000000')

def test_sfo_breakeven_small_estate(sfo_engine):
    # $20M AUM at 1% is $200k. SFO costs $1M.
    result = sfo_engine.run_breakeven_analysis(Decimal('20000000'))
    assert result['is_sfo_economically_viable'] is False

def test_mfo_pro_rata_allocation(mfo_allocator):
    overhead = Decimal('100000')
    family_aums = {
        "FAMILY_A": Decimal('80000000'), 
        "FAMILY_B": Decimal('20000000')
    }
    result = mfo_allocator.split_monthly_overhead(overhead, family_aums, method='PRO_RATA')
    # Family A should pay 80% ($80k)
    assert result[0]['amount'] == Decimal('80000.00')
    assert result[1]['amount'] == Decimal('20000.00')
