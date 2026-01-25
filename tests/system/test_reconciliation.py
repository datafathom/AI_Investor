import pytest
from services.banking.reconciliation_service import get_reconciliation_service

def test_reconciliation_singleton():
    s1 = get_reconciliation_service()
    s2 = get_reconciliation_service()
    assert s1 is s2

def test_recon_matching_logic():
    service = get_reconciliation_service()
    report = service.perform_reconciliation("mock_token")
    
    # In the service, Starbucks NYC (-42.50) should match Starbucks Coffee (-42.50)
    assert report["matched_count"] >= 2
    assert "accuracy" in report
    assert report["accuracy"] > 0

def test_unreconciled_items():
    service = get_reconciliation_service()
    report = service.perform_reconciliation("mock_token")
    
    # Bank has Netflix (-10.99) which is NOT in ledger
    bank_unm = [item["desc"] for item in report["unreconciled_bank"]]
    assert any("Netflix" in d for d in bank_unm)
    
    # Ledger has AWS (-120.00) which is NOT in bank
    ledger_unm = [item["desc"] for item in report["unreconciled_ledger"]]
    assert any("AWS" in d for d in ledger_unm)
