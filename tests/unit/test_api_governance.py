import pytest
import asyncio
import time
from services.system.api_governance import APIGovernor

@pytest.mark.asyncio
async def test_governor_throttling():
    governor = APIGovernor()
    # Override limit for testing
    governor.LIMITS["TEST_PROV"] = {"per_minute": 2, "per_day": 10}
    
    # Fill slots
    governor.report_usage("TEST_PROV")
    governor.report_usage("TEST_PROV")
    
    # Third call should trigger a wait
    start = time.time()
    wait_task = asyncio.create_task(governor.wait_for_slot("TEST_PROV"))
    
    # Wait a bit to ensure it's stuck
    await asyncio.sleep(1)
    assert not wait_task.done()
    
    # Simulate time passing by clearing minute stats
    stats = governor._get_stats("TEST_PROV")
    stats["minute"] = [] # Clear slots
    
    await asyncio.wait_for(wait_task, timeout=3.0)
    end = time.time()
    assert end - start >= 1.0 # Waited at least 1s
    assert wait_task.done()

@pytest.mark.asyncio
async def test_governor_daily_limit():
    governor = APIGovernor()
    governor.LIMITS["DAILY_PROV"] = {"per_minute": 10, "per_day": 1}
    
    await governor.wait_for_slot("DAILY_PROV")
    governor.report_usage("DAILY_PROV")
    
    with pytest.raises(RuntimeError, match="Daily limit exceeded"):
        await governor.wait_for_slot("DAILY_PROV")
