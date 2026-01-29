import pytest
from datetime import datetime, timedelta
from services.compliance.wash_sale_validator import WashSaleValidator

def test_wash_sale_violation():
    svc = WashSaleValidator()
    ticker = "SPY"
    loss_date = datetime(2025, 1, 15)
    # Buy within 30 days window
    recent_buys = [{"ticker": "SPY", "date": datetime(2025, 1, 10), "amount": 1000}]
    res = svc.check_wash_sale(ticker, loss_date, recent_buys)
    assert res["is_safe"] == False
    assert res["verification_status"] == "WASH_SALE_DETECTED"

def test_wash_sale_safe():
    svc = WashSaleValidator()
    ticker = "SPY"
    loss_date = datetime(2025, 1, 15)
    # Buy outside 30 days window (e.g. 40 days before)
    recent_buys = [{"ticker": "SPY", "date": datetime(2024, 12, 1), "amount": 1000}]
    res = svc.check_wash_sale(ticker, loss_date, recent_buys)
    assert res["is_safe"] == True
    assert res["verification_status"] == "VALIDATED"
