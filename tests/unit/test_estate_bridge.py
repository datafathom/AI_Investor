import pytest
from services.estate.asset_bridge import EstateAssetBridge

def test_trust_exposure_tax_high():
    svc = EstateAssetBridge()
    asset = {"ticker": "EQIX", "asset_class": "REIT", "market_value": 50000}
    res = svc.expose_to_trust(asset, "REVOCABLE")
    assert res["tax_efficiency_status"] == "HIGH"
    assert res["eligibility_for_step_up"] == True

def test_trust_exposure_standard():
    svc = EstateAssetBridge()
    asset = {"ticker": "AAPL", "asset_class": "EQUITY", "market_value": 20000}
    res = svc.expose_to_trust(asset, "IRREVOCABLE")
    assert res["tax_efficiency_status"] == "STANDARD"
    assert res["eligibility_for_step_up"] == False
