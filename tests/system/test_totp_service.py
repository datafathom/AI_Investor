import pytest
import pyotp
from services.system.totp_service import get_totp_service

def test_totp_singleton():
    s1 = get_totp_service()
    s2 = get_totp_service()
    assert s1 is s2

def test_generate_secret():
    service = get_totp_service()
    secret = service.generate_new_secret()
    assert len(secret) == 32
    # Verify it's valid base32
    import base64
    base64.b32decode(secret)

def test_verification_logic():
    service = get_totp_service()
    secret = service.generate_new_secret()
    totp = pyotp.TOTP(secret)
    current_code = totp.now()
    
    assert service.verify_code(secret, current_code) is True
    assert service.verify_code(secret, "000000") is False

def test_mock_hardware_token():
    import os
    os.environ["YUBIKEY_MOCK"] = "1"
    service = get_totp_service()
    # Any secret should work with the mock code
    assert service.verify_code("ANY_SECRET", "999999") is True

def test_provisioning_uri():
    service = get_totp_service()
    secret = service.generate_new_secret()
    uri = service.get_provisioning_uri(secret, "test_user")
    assert "otpauth://totp/" in uri
    assert "test_user" in uri
    assert "AI%20Investor" in uri
