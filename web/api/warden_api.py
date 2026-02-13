from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/warden", tags=["Warden"])

@router.get('/threats')
async def get_active_threats():
    """Get active security threats."""
    return {"success": True, "data": [
        {"id": "thr_01", "type": "DDOS_ATTEMPT", "source": "145.2.1.99", "location": "CN", "status": "BLOCKED", "rps": 5000},
        {"id": "thr_02", "type": "SQL_INJECTION", "source": "88.1.1.2", "location": "RU", "status": "MITIGATED", "payload": "' OR 1=1 --"}
    ]}

@router.post('/actions/block')
async def block_ip(ip: str):
    """Manually block an IP address."""
    return {"success": True, "data": {"ip": ip, "status": "BLOCKED"}}
