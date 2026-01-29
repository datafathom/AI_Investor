import pytest
from decimal import Decimal
from services.compliance.fatca_compliance_svc import FATCAComplianceService
from services.tax.exit_tax_engine import ExitTaxEngine
from services.compliance.restriction_engine import RestrictionEngine

@pytest.fixture
def fatca_svc():
    return FATCAComplianceService()

@pytest.fixture
def exit_tax_engine():
    return ExitTaxEngine()

@pytest.fixture
def restriction_engine():
    return RestrictionEngine()

def test_fatca_threshold_checks(fatca_svc):
    # $20k -> FBAR required, FATCA not
    result = fatca_svc.check_reporting_thresholds(Decimal('20000'))
    assert result['requires_fbar_filing'] is True
    assert result['requires_8938_filing'] is False

def test_exit_tax_covered_expatriate_status(exit_tax_engine):
    # $3M NW -> Covered
    result = exit_tax_engine.determine_expat_status(Decimal('3000000'), Decimal('100000'))
    assert result['is_covered_expatriate'] is True

def test_exit_tax_phantom_sale(exit_tax_engine):
    # $10M value, $5M basis = $5M gain. Exclusion $866k. Tax on $4.134M @ 23.8% ~ $983k
    result = exit_tax_engine.calculate_phantom_sale_liability(Decimal('10000000'), Decimal('5000000'))
    assert result['taxable_exit_gain'] == Decimal('4134000.00')
    assert result['estimated_tax_bill'] > Decimal('980000')

def test_rule144_selling_limit_calc(restriction_engine):
    # 100M shares, 2M vol. 1% = 1M. Vol = 2M. Max = 2M.
    result = restriction_engine.check_rule144_selling_limit(100000000, 2000000)
    assert result['max_quarterly_sale_qty'] == 2000000
    assert result['restriction_basis'] == "ADTV"
