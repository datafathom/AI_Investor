import pytest
from services.legal.ownership_resolver import LegalOwnershipResolver

def test_resolve_individual():
    svc = LegalOwnershipResolver()
    res = svc.resolve_tax_entity("INDIVIDUAL")
    assert res["entity_type"] == "PERSON"
    assert res["is_pass_through"] == True

def test_resolve_revocable_trust():
    svc = LegalOwnershipResolver()
    res = svc.resolve_tax_entity("REVOCABLE_TRUST")
    assert res["entity_type"] == "PERSON_GRANTOR"
    assert res["is_pass_through"] == True

def test_resolve_irrevocable_trust():
    svc = LegalOwnershipResolver()
    res = svc.resolve_tax_entity("IRREVOCABLE_TRUST")
    assert res["entity_type"] == "TRUST_ENTITY"
    assert res["is_pass_through"] == False
    assert res["requires_separate_tax_filing"] == True
