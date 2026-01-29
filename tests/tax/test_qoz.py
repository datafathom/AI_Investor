import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from services.tax.qoz_service import QOZService, QOZInvestment

def test_qoz_basis_step_up():
    service = QOZService()
    # Investment made 6 years ago
    six_years_ago = datetime.now() - timedelta(days=6*365.25)
    inv = QOZInvestment(
        investment_id="QOZ_001",
        amount=Decimal("100000"),
        investment_date=six_years_ago,
        zone_id="ZONE_A"
    )
    service.add_investment(inv)
    
    basis = service.get_adjusted_basis("QOZ_001")
    # 5 years hit, 7 years not hit -> 10% step up
    assert basis == Decimal("10000")

def test_qoz_7_year_step_up():
    service = QOZService()
    # Investment made 8 years ago
    eight_years_ago = datetime.now() - timedelta(days=8*365.25)
    inv = QOZInvestment(
        investment_id="QOZ_002",
        amount=Decimal("100000"),
        investment_date=eight_years_ago,
        zone_id="ZONE_B"
    )
    service.add_investment(inv)
    
    basis = service.get_adjusted_basis("QOZ_002")
    # 7 years hit -> 15% step up
    assert basis == Decimal("15000")

def test_qoz_2026_cliff():
    service = QOZService()
    # Investment made on Jan 1, 2019
    start_2019 = datetime(2019, 1, 1)
    inv = QOZInvestment(
        investment_id="QOZ_2019",
        amount=Decimal("100000"),
        investment_date=start_2019,
        zone_id="ZONE_C"
    )
    service.add_investment(inv)
    
    # By Dec 31, 2026, it will be 7.99 years -> 15% step up
    taxable = service.calculate_taxable_gain_2026("QOZ_2019")
    # 100,000 - 15,000 = 85,000
    assert taxable == Decimal("85000")

def test_qoz_10_year_exclusion():
    service = QOZService()
    # Investment made 11 years ago
    eleven_years_ago = datetime.now() - timedelta(days=11*365.25)
    inv = QOZInvestment(
        investment_id="QOZ_OLD",
        amount=Decimal("100000"),
        investment_date=eleven_years_ago,
        zone_id="ZONE_D"
    )
    service.add_investment(inv)
    
    assert service.is_eligible_for_full_exclusion("QOZ_OLD") is True
    assert service.is_eligible_for_full_exclusion("QOZ_2019") is False
