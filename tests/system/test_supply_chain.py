import pytest
import os
import json
from services.system.supply_chain_service import get_supply_chain_service

def test_supply_chain_singleton():
    s1 = get_supply_chain_service()
    s2 = get_supply_chain_service()
    assert s1 is s2

def test_audit_execution():
    service = get_supply_chain_service()
    result = service.run_audit()
    assert result["status"] == "Secure"
    assert "last_scan" in result
    assert os.path.exists(service.report_path)

def test_sbom_generation():
    service = get_supply_chain_service()
    success = service.generate_sbom()
    assert success is True
    assert os.path.exists(service.sbom_path)
    
    with open(service.sbom_path, 'r') as f:
        data = json.load(f)
        assert "dependencies" in data
        assert len(data["dependencies"]) > 0

def test_get_status():
    service = get_supply_chain_service()
    service.run_audit()
    status = service.get_audit_status()
    assert status["status"] == "Secure"
    assert "vulnerabilities" in status
