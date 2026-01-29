import pytest
from uuid import UUID
from decimal import Decimal
from services.legal.ownership_separator import OwnershipSeparator
from services.compliance.solvency_validator import SolvencyValidator

@pytest.fixture
def separator():
    return OwnershipSeparator()

@pytest.fixture
def solvency_validator():
    return SolvencyValidator()

def test_ownership_separation_dapt(separator):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    # DAPT should be legally separated
    result = separator.verify_separation(trust_id, 'DAPT')
    assert result['status'] == "LEGALLY_SEPARATED"
    assert result['is_protected'] is True

def test_solvency_validator_passed(solvency_validator):
    # $1M assets, $100k liabilities, $500k transfer -> $500k remaining. Ratio 5.0 (Pass)
    result = solvency_validator.validate_solvency_post_transfer(Decimal('1000000'), Decimal('100000'), Decimal('500000'))
    assert result['is_valid_solvency'] is True
    assert result['solvency_ratio'] == 5.0

def test_solvency_validator_failed(solvency_validator):
    # $1M assets, $800k liabilities, $500k transfer -> $500k remaining. Ratio 0.625 (Fail)
    result = solvency_validator.validate_solvency_post_transfer(Decimal('1000000'), Decimal('800000'), Decimal('500000'))
    assert result['is_valid_solvency'] is False
    assert result['solvency_ratio'] < 1.0
