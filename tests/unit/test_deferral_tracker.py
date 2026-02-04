import pytest
from services.tax.deferral_tracker import DeferralTracker
from schemas.private_banking_client import TaxDeferralStrategy
from uuid import uuid4
from datetime import date, timedelta

def test_deferral_expiry_warning():
    tracker = DeferralTracker()
    strategy = TaxDeferralStrategy(
        client_id=uuid4(),
        strategy_type="1031_EXCHANGE",
        gain_deferred=500000.0,
        initiation_date=date.today(),
        expiration_date=date.today() + timedelta(days=10) # 10 days left
    )
    days = tracker.calculate_days_remaining(strategy)
    assert days == 10

def test_deferral_savings_estimate():
    tracker = DeferralTracker()
    # 1M gain deferred @ 20% cap gains rate
    savings = tracker.estimate_tax_savings(1000000, 0.20)
    assert savings == 200000.0
