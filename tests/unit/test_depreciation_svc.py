import pytest
from services.tax.depreciation_service import DepreciationService

def test_depreciation_residential():
    svc = DepreciationService()
    # 275,000 building -> 10,000/yr
    assert svc.calculate_annual_deduction(275000, "RESIDENTIAL") == 10000.0

def test_tax_shield_benefit():
    svc = DepreciationService()
    # 10k deduction at 37% bracket -> $3,700 savings
    assert svc.calculate_tax_shield(10000, 0.37) == 3700.0
