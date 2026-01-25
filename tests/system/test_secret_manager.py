import os
import pytest
from services.system.secret_manager import get_secret_manager

def test_secret_manager_singleton():
    sm1 = get_secret_manager()
    sm2 = get_secret_manager()
    assert sm1 is sm2

def test_get_secret_default():
    sm = get_secret_manager()
    assert sm.get_secret("NON_EXISTENT_KEY", "default_val") == "default_val"

def test_get_secret_real_env():
    os.environ["TEST_SECRET"] = "my_secret_123"
    sm = get_secret_manager()
    assert sm.get_secret("TEST_SECRET") == "my_secret_123"

def test_masking_logic():
    sm = get_secret_manager()
    # Long secret
    os.environ["LONG_SECRET"] = "secret_long_value"
    masked = sm.get_masked_secret("LONG_SECRET")
    assert masked == "se****ue"
    
    # Short secret
    os.environ["SHORT"] = "123"
    assert sm.get_masked_secret("SHORT") == "****"

def test_db_credentials():
    sm = get_secret_manager()
    creds = sm.get_db_credentials()
    assert "url" in creds
    assert "masked_url" in creds
    assert "postgresql" in creds["url"]

def test_status():
    sm = get_secret_manager()
    status = sm.get_status()
    assert status["status"] == "Active"
    assert "engine" in status
