import pytest
from decimal import Decimal
from services.real_estate.syndication_service import SyndicationService

def test_create_syndication():
    service = SyndicationService()
    record = service.create_syndication("Project X", Decimal("100000"))
    assert record.name == "Project X"
    assert record.initial_investment == Decimal("100000")
    assert record.current_basis == Decimal("100000")

def test_record_distribution():
    service = SyndicationService()
    record = service.create_syndication("Project Y", Decimal("200000"))
    
    # Rental income does not reduce basis
    service.record_distribution(record.id, Decimal("5000"), "Rental income")
    updated_record = service.records[record.id]
    assert updated_record.cumulative_distributions == Decimal("5000")
    assert updated_record.current_basis == Decimal("200000")
    
    # Return of capital reduces basis
    service.record_distribution(record.id, Decimal("10000"), "Return of capital")
    assert updated_record.cumulative_distributions == Decimal("15000")
    assert updated_record.current_basis == Decimal("190000")

def test_calculate_tax_recapture():
    service = SyndicationService()
    record = service.create_syndication("Project Z", Decimal("100000"))
    
    # Simulate $20k return of capital (depreciation recapture potential)
    service.record_distribution(record.id, Decimal("20000"), "Return of capital")
    
    # Sale price $150k
    recapture_info = service.calculate_tax_recapture(record.id, Decimal("150000"))
    
    # current_basis = 80,000
    # total_gain = 150,000 - 80,000 = 70,000
    # recapture_amount = 100,000 - 80,000 = 20,000
    # capital_gain_amount = 70,000 - 20,000 = 50,000
    
    assert recapture_info["total_gain"] == Decimal("70000")
    assert recapture_info["recapture_amount"] == Decimal("20000")
    assert recapture_info["capital_gain_amount"] == Decimal("50000")
