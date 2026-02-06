from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, List
import logging
from arq.connections import RedisSettings
from arq.jobs import Job

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)

@router.post("/run")
async def run_task(request: Request, mission_data: Dict[str, Any]):
    """Enqueues an agent mission."""
    arq_pool = request.app.state.arq_pool
    if not arq_pool:
        raise HTTPException(status_code=503, detail="Task queue unavailable")
    
    job = await arq_pool.enqueue_job('run_agent_logic', mission_data)
    return {"status": "accepted", "job_id": job.job_id}

@router.get("/status")
async def get_queue_status(request: Request):
    """Returns the current state of the worker queue."""
    arq_pool = request.app.state.arq_pool
    if not arq_pool:
        raise HTTPException(status_code=503, detail="Task queue unavailable")
    
    # ARQ doesn't provide a direct "get all jobs" method out of the box easily 
    # without iterating keys, but we can return some basic info if we track them.
    # For now, we'll return a mock list or use Redis keys if we find the pattern.
    
    # Real implementation would query Redis for arq:job:<id> keys
    # For now, let's provide a structured response
    return {
        "status": "online",
        "jobs": [] # Placeholder for real job tracking
    }

@router.post("/kill/{job_id}")
async def kill_job(request: Request, job_id: str):
    """Aborts a specific job."""
    arq_pool = request.app.state.arq_pool
    if not arq_pool:
        raise HTTPException(status_code=503, detail="Task queue unavailable")
    
    try:
        job = Job(job_id, arq_pool)
        success = await job.abort()
        return {"status": "success" if success else "failed", "job_id": job_id}
    except Exception as e:
        logger.error(f"Failed to kill job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
