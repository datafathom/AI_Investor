import pytest
from services.private_banking.qualifier import PrivateBankingQualifier
from uuid import uuid4

def test_pb_qualification_family_office():
    qualifier = PrivateBankingQualifier()
    # $120M
    res = qualifier.qualify_client(uuid4(), 120000000)
    assert res["qualified"] == True
    assert res["tier"] == "FAMILY_OFFICE"

def test_pb_qualification_none():
    qualifier = PrivateBankingQualifier()
    # $5M - not enough for PRIVATE
    res = qualifier.qualify_client(uuid4(), 5000000)
    assert res["qualified"] == False
    assert res["tier"] == "NONE"
