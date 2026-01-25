import pytest
from services.security.compliance_service import ComplianceService, AuditLog
import hashlib
import json

@pytest.mark.asyncio
async def test_audit_log_hash_chaining():
    service = ComplianceService()
    # Mock data already has a chain of 5 logs
    logs = await service.get_audit_logs()
    assert len(logs) == 5
    
    # Verify initial chain
    integrity = await service.verify_log_integrity()
    assert integrity["is_valid"] is True
    
    # Add new log
    new_log = await service.add_audit_log({
        "action": "TEST_ACTION",
        "resource": "TEST_RESOURCE",
        "severity": "info"
    })
    
    assert new_log.prev_hash == logs[-1].hash
    assert new_log.hash == new_log.calculate_hash()
    
    integrity = await service.verify_log_integrity()
    assert integrity["is_valid"] is True

@pytest.mark.asyncio
async def test_audit_log_tamper_detection():
    service = ComplianceService()
    logs = await service.get_audit_logs()
    
    # Tamper with a log
    logs[2].action = "TAMPERED"
    
    integrity = await service.verify_log_integrity()
    assert integrity["is_valid"] is False
    assert any("Data tampered" in err for err in integrity["errors"])

@pytest.mark.asyncio
async def test_abuse_detection_spoofing():
    service = ComplianceService()
    
    # Add an order with low latency
    log_data = {
        "action": "ORDER_PLACEMENT",
        "resource": "TRADING_ENGINE",
        "severity": "info",
        "details": {"latency_ms": 4, "agent_id": "Bot-99"}
    }
    
    await service.add_audit_log(log_data)
    
    alerts = await service.get_sar_alerts()
    spoofing_alerts = [a for a in alerts if a.type == "spoofing" and a.agent_id == "Bot-99"]
    assert len(spoofing_alerts) == 1
    assert spoofing_alerts[0].evidence_score == 0.9

@pytest.mark.asyncio
async def test_compliance_score_calculation():
    service = ComplianceService()
    initial_score = await service.get_compliance_score()
    
    # Initially 3 pending alerts (2 mock aml/insider + 1 mock spoofing)
    assert initial_score == 100 - (3 * 5)
    
    # Resolve one alert
    alerts = await service.get_sar_alerts()
    await service.update_sar_status(alerts[0].id, "reviewed")
    
    new_score = await service.get_compliance_score()
    assert new_score == initial_score + 5
