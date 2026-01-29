import pytest
from services.legal.ppli_structure import PPLIStructureValidator

def test_optimal_structure():
    svc = PPLIStructureValidator()
    res = svc.validate_ownership("IRREVOCABLE_TRUST", "PPLI")
    assert res["is_estate_tax_shielded"] == True
    assert res["ownership_status"] == "OPTIMAL_ILIT"

def test_suboptimal_structure():
    svc = PPLIStructureValidator()
    res = svc.validate_ownership("INDIVIDUAL", "PPLI")
    assert res["is_estate_tax_shielded"] == False
    assert res["recommendation"] == "TRANSFER_TO_ILIT"
