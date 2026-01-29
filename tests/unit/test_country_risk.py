import pytest
from services.risk.country_risk import CountryRiskService

def test_country_risk_lookup():
    svc = CountryRiskService()
    res = svc.evaluate_country("RU")
    assert res["sanction_risk"] == "CRITICAL"
    assert res["repatriation_risk"] == "CRITICAL"

def test_low_risk_lookup():
    svc = CountryRiskService()
    res = svc.evaluate_country("SG")
    assert res["sanction_risk"] == "LOW"
    assert res["cap_controls"] == False
