import pytest
from services.retirement.compounding_buffer import CompoundingBufferCalculator

def test_buffer_requirement():
    svc = CompoundingBufferCalculator()
    # 1M, 3% inflation needed to keep real value flat.
    assert svc.calculate_required_buffer(1000000, 0.03) == 30000.0
