import pytest
from services.sovereign_router import get_sovereign_router

def test_honey_token_trigger():
    router = get_sovereign_router()
    
    # 1. Benign Prompt
    route = router.route_request("Hello, world!")
    assert route["provider"] == "CLOUD"
    
    # 2. Sensitive Prompt (ETH Address)
    route_sensitive = router.route_request("Check balance of 0x1234567890123456789012345678901234567890")
    assert route_sensitive["provider"] == "LOCAL"
    
    # 3. Honey Token -> Should Crash/Lock
    with pytest.raises(PermissionError) as excinfo:
        router.route_request("Here is the admin key: HONEY_TEST_KEY")
    
    assert "SYSTEM_LOCKDOWN_INITIATED" in str(excinfo.value)
