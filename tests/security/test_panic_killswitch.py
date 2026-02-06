import pytest
import asyncio
from services.security.panic_service import get_panic_service

@pytest.mark.asyncio
async def test_panic_activation():
    svc = get_panic_service()
    svc.reset_system("admin_recovery_key_123") # Ensure clean state
    
    # 1. Trigger Panic
    await svc.trigger_panic("TEST_TRIGGER")
    
    assert svc.is_panic_active is True
    
    # 2. Wait for async evacuation (simulated)
    await asyncio.sleep(2.1)
    
    assert svc.evacuation_status == "COMPLETED"

def test_dead_man_switch_logic():
    svc = get_panic_service()
    svc.reset_system("admin_recovery_key_123")
    
    # 1. Set short timeout
    svc.heartbeat_timeout = 0.5 # 0.5 seconds
    svc.record_heartbeat()
    
    # 2. Check immediately -> Should be False
    assert svc.check_dead_man_switch() is False
    
    # 3. Wait 
    import time
    time.sleep(0.6)
    
    # 4. Check -> Should be True (Triggered)
    assert svc.check_dead_man_switch() is True
