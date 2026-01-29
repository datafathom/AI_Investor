import pytest
from services.billing.proration_service import ProrationService
from datetime import date

def test_full_quarter_proration():
    service = ProrationService()
    # 90 days in a quarter (approx)
    start = date(2026, 1, 1)
    end = date(2026, 3, 31) # 90 days total
    factor = service.calculate_proration_factor(start, end, 90)
    assert factor == 1.0

def test_partial_month_proration():
    service = ProrationService()
    # 45 days / 90 days = 0.5
    start = date(2026, 1, 1)
    end = date(2026, 2, 14) 
    factor = service.calculate_proration_factor(start, end, 90)
    assert factor == 0.5
