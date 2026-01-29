import pytest
from services.legal.modification_gate import TrustModificationGate

def test_revocable_all_allowed():
    svc = TrustModificationGate()
    # Revocable allows everything
    assert svc.can_perform_action("REVOCABLE", "WITHDRAW")["is_allowed"] == True
    assert svc.can_perform_action("REVOCABLE", "AMEND")["is_allowed"] == True

def test_irrevocable_restrictions():
    svc = TrustModificationGate()
    # Irrevocable blocks withdrawals/amendments
    assert svc.can_perform_action("IRREVOCABLE", "WITHDRAW")["is_allowed"] == False
    assert svc.can_perform_action("IRREVOCABLE", "AMEND")["is_allowed"] == False
    # But allows investment management
    assert svc.can_perform_action("IRREVOCABLE", "REBALANCE")["is_allowed"] == True
