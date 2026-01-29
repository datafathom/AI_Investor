import pytest
from decimal import Decimal
from services.estate.legacy_simulator import LegacySimulator

@pytest.fixture
def simulator():
    return LegacySimulator()

def test_simulator_singleton():
    s1 = LegacySimulator()
    s2 = LegacySimulator()
    assert s1 is s2

def test_run_projection(simulator):
    initial = Decimal('1000000')
    result = simulator.run_projection(initial, 0.07, 2, 0.40)
    
    assert 'dynasty_value' in result
    assert 'taxable_value' in result
    assert result['dynasty_value'] > result['taxable_value']
    assert result['tax_savings'] > 0
