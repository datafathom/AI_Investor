import pytest
from uuid import uuid4
from services.risk.custodian_risk_engine import CustodianRiskEngine
from services.custody.drs_transfer_mgr import DRSTransferManager

@pytest.fixture
def risk_engine():
    return CustodianRiskEngine()

@pytest.fixture
def drs_mgr():
    return DRSTransferManager()

def test_custodian_solvency_alert(risk_engine):
    # 600bps -> CRITICAL
    result = risk_engine.assess_custodian_solvency(600)
    assert result['solvency_status'] == "CRITICAL"
    assert result['audit_priority'] == "URGENT"

def test_drs_verification_logic(drs_mgr):
    assert drs_mgr.verify_legal_title("DRS") is True
    assert drs_mgr.verify_legal_title("STREET_NAME") is False
    
def test_drs_transfer_initiation(drs_mgr):
    asset_id = uuid4()
    broker_id = uuid4()
    result = drs_mgr.initiate_drs_transfer(asset_id, broker_id, 100)
    assert result['status'] == "INITIATED"
    assert result['shares'] == 100
