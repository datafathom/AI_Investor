import pytest
from services.tax.priority_logic import TaxPriorityLogic

@pytest.fixture
def priority_logic():
    return TaxPriorityLogic()

def test_determine_harvest_priority_st(priority_logic):
    # Short-term gains should trigger ST realization priority
    result = priority_logic.determine_harvest_priority(10000.0, 50000.0)
    assert result == "ST_REALIZATION"

def test_determine_harvest_priority_lt_only(priority_logic):
    # If no ST gains, default to LT
    result = priority_logic.determine_harvest_priority(0.0, 50000.0)
    assert result == "LT_REALIZATION"
