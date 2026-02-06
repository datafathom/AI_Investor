import pytest
from services.security.webauthn_service import get_webauthn_service

def test_approval_flow():
    svc = get_webauthn_service()
    
    # 1. Create Request
    req_id = svc.create_approval_request("mssn_123", "deploy_exploit", {})
    assert req_id is not None
    assert len(svc.get_pending_requests()) == 1
    
    # 2. Verify with valid signature (Mock)
    success = svc.verify_and_approve(req_id, "valid_sig_abc", "pub_key_xyz")
    assert success is True
    
    # 3. Request should no longer be pending
    assert len(svc.get_pending_requests()) == 0
    assert svc.pending_approvals[req_id]["status"] == "APPROVED"

def test_rejection_flow():
    svc = get_webauthn_service()
    req_id = svc.create_approval_request("mssn_456", "transfer_assets", {})
    
    # Reject
    svc.reject_request(req_id)
    assert svc.pending_approvals[req_id]["status"] == "REJECTED"
