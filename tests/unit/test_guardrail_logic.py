"""
Unit tests for Risk Guardrail Logic.
Verifies integrity hashing and safe mode fallback.
"""
import pytest
from services.security.config_integrity import ConfigIntegrity
from services.risk.config_manager import ConfigManager

def test_hash_consistency():
    config = {"id": "conf_1", "max_risk": 0.01}
    hash1 = ConfigIntegrity.generate_state_hash(config)
    hash2 = ConfigIntegrity.generate_state_hash(config)
    
    assert hash1 == hash2
    assert len(hash1) == 64 # SHA-256 length

def test_config_hydration_success():
    manager = ConfigManager()
    config = {"id": "conf_1", "max_position_size_pct": 0.01}
    valid_hash = ConfigIntegrity.generate_state_hash(config)
    
    manager.hydrate_from_db(config, valid_hash)
    
    assert manager.safe_mode == False
    assert manager.get_param("max_position_size_pct") == 0.01

def test_config_hydration_tamper_detection():
    manager = ConfigManager()
    config = {"id": "conf_1", "max_position_size_pct": 0.05} # Tampered (original 0.01)
    wrong_hash = ConfigIntegrity.generate_state_hash({"id": "conf_1", "max_position_size_pct": 0.01})
    
    manager.hydrate_from_db(config, wrong_hash)
    
    assert manager.safe_mode == True
    # Safe Mode should cap risk at 0.0
    assert manager.get_param("max_position_size_pct") == 0.0
