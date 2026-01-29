"""
E2E System Stability Tests.
"""
import pytest
import os
import time
from services.monitoring.latency_monitor import latency_monitor
from services.process_monitor import ProcessMonitor
from services.agents.heartbeat_service import heartbeat_service

def test_latency_recording():
    latency_monitor.record_latency("EUR/USD", time.time() - 0.050) # 50ms
    avg = latency_monitor.get_average_latency("EUR/USD")
    assert 0.040 < avg < 0.060

def test_process_monitoring():
    # Test on self
    pid = os.getpid()
    stats = ProcessMonitor.get_process_stats(pid)
    assert stats['pid'] == pid
    assert stats['mem_mb'] > 0

@pytest.mark.asyncio
async def test_heartbeat_flow():
    agent_id = "test-agent-alpha"
    await heartbeat_service.record_heartbeat(agent_id, "starting")
    agents = await heartbeat_service.get_all_agents()
    
    match = next((a for a in agents if a['agent_id'] == agent_id), None)
    assert match is not None
    assert match['status'] == 'starting'
