import pytest
from services.system.social_auth_service import get_social_auth_service

def test_social_auth_singleton():
    s1 = get_social_auth_service()
    s2 = get_social_auth_service()
    assert s1 is s2

def test_initiate_auth_flow():
    service = get_social_auth_service()
    url = service.initiate_auth_flow("paypal")
    assert "paypal" in url
    assert "authorize" in url

def test_handle_callback_existing_user():
    service = get_social_auth_service()
    # "paypal_mock_123" is pre-linked to admin (user_id 1)
    result = service.handle_callback("paypal", "123_some_code")
    
    assert result["user"]["username"] == "admin"
    assert result["user"]["id"] == 1
    assert result["new_user"] is False
    assert "token" in result

def test_handle_callback_new_user():
    service = get_social_auth_service()
    # A new code should trigger new user creation
    result = service.handle_callback("stripe", "new_user_999")
    
    assert "stripe" in result["user"]["username"]
    assert result["new_user"] is True
    assert result["user"]["role"] == "trader"
    assert "token" in result

def test_account_persistence():
    service = get_social_auth_service()
    code = "persist_test_1"
    result1 = service.handle_callback("square", code)
    user_id = result1["user"]["id"]
    
    # Second time with same code (generating same vendor_id) should be existing user
    result2 = service.handle_callback("square", code)
    assert result2["user"]["id"] == user_id
    assert result2["new_user"] is False
