from fastapi import APIRouter
import time
import random
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/orchestrator", tags=["Orchestrator & Sovereign OS"])

# --- Tactical Command ---
@router.get('/global-state')
async def get_os_global_state():
    """Get global OS state for 3D sphere."""
    return {"success": True, "data": {
        "status": "OPERATIONAL",
        "pulse": "NORMAL",
        "active_departments": 18,
        "active_services": 133,
        "defcon": 5,
        "critical_actions": ["Trader executing VWAP on NVDA", "Risk analyzing Volatility spike"],
        "departments": [
            {"id": "d_01", "name": "Trading", "health": 98, "load": 45},
            {"id": "d_02", "name": "Risk", "health": 100, "load": 30},
            {"id": "d_03", "name": "Research", "health": 95, "load": 60},
            {"id": "d_04", "name": "Compliance", "health": 100, "load": 10}
        ]
    }}

@router.post('/tactical/action')
async def execute_global_command(cmd: str):
    """Execute global tactical command."""
    return {"success": True, "data": {"status": "EXECUTED", "command": cmd, "timestamp": time.time()}}

# --- Autonomy Control ---
@router.get('/constraints')
async def list_hard_constraints():
    """List hard constraints."""
    return {"success": True, "data": [
        {"id": "c_01", "rule": "No Margin Usage > 20%", "status": "ACTIVE", "locked": True},
        {"id": "c_02", "rule": "Max Single Stock Exposure 15%", "status": "ACTIVE", "locked": False},
        {"id": "c_03", "rule": "No Shorting on Earnings Day", "status": "ACTIVE", "locked": False}
    ]}

@router.put('/autonomy/level')
async def set_sovereign_autonomy_level(level: int):
    """Set autonomy level (0-10)."""
    return {"success": True, "data": {"level": level, "mode": "Co-Pilot" if level < 8 else "Sovereign"}}

# --- Consensus Visualizer ---
@router.get('/consensus/active')
async def get_ongoing_consensus_debates():
    """Get active consensus debates."""
    return {"success": True, "data": [
        {
            "id": "vote_01",
            "topic": "Increase Crypto Allocation to 10%",
            "status": "VOTING",
            "progress": 0.65,
            "threshold": 0.70,
            "votes": [
                {"agent": "Risk Manager", "vote": "NO", "reason": "Volatility too high"},
                {"agent": "Crypto Analyst", "vote": "YES", "reason": "Bullish momentum signal"},
                {"agent": "Macro Strategist", "vote": "YES", "reason": "Inflation hedge"}
            ]
        }
    ]}

# --- Unified Alerts ---
@router.get('/alerts/unified')
async def get_all_active_alerts():
    """Get unified alerts."""
    return {"success": True, "data": [
        {"id": "a_01", "severity": "CRITICAL", "source": "Security", "msg": "API Key Rotation Required", "time": "2 mins ago"},
        {"id": "a_02", "severity": "WARNING", "source": "Market", "msg": "VIX Breakout > 25", "time": "15 mins ago"},
        {"id": "a_03", "severity": "INFO", "source": "System", "msg": "Backup Completed", "time": "1 hour ago"}
    ]}

@router.post('/alerts/clear')
async def clear_all_notifications():
    """Clear all alerts."""
    return {"success": True, "data": {"status": "CLEARED"}}

# --- OS Health & Stats ---
@router.get('/stats/usage')
async def get_system_utilization():
    """Get system resource usage."""
    return {"success": True, "data": {
        "cpu_usage": 32,
        "ram_usage": 45,
        "disk_usage": 60,
        "db_connections": 12,
        "token_usage_cost": 12.50,
        "uptime": "14d 10h 32m"
    }}

@router.get('/health/heartbeat')
async def check_core_heartbeat():
    """Check core heartbeat."""
    return {"success": True, "data": {"status": "ALIVE", "latency": "12ms"}}
