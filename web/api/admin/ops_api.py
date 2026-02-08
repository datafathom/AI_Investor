import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from services.operations.job_scheduler import get_job_scheduler, JobScheduler

router = APIRouter(prefix="/ops", tags=["Admin", "Operations"])

# --- Pydantic Models ---

class Job(BaseModel):
    id: str
    name: str
    schedule: str
    last_run: Optional[str] = None
    status: str
    type: str
    description: Optional[str] = None

class JobHistory(BaseModel):
    execution_id: str
    job_id: str
    job_name: str
    started_at: str
    ended_at: Optional[str] = None
    duration_ms: int
    status: str
    logs: str

class ScheduleUpdate(BaseModel):
    schedule: str

# --- Dependency ---

def get_scheduler():
    return get_job_scheduler()

# --- Endpoints ---

@router.get("/jobs", response_model=List[Job])
async def list_jobs(scheduler: JobScheduler = Depends(get_scheduler)):
    return scheduler.get_jobs()

@router.get("/jobs/{job_id}", response_model=Job)
async def get_job_details(job_id: str, scheduler: JobScheduler = Depends(get_scheduler)):
    job = scheduler.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/jobs/{job_id}/trigger", response_model=JobHistory)
async def trigger_job(job_id: str, scheduler: JobScheduler = Depends(get_scheduler)):
    try:
        result = await scheduler.trigger_job(job_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error triggering job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/jobs/{job_id}", response_model=Dict[str, str])
async def update_job_schedule(job_id: str, update: ScheduleUpdate, scheduler: JobScheduler = Depends(get_scheduler)):
    success = scheduler.update_job_schedule(job_id, update.schedule)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "success", "message": f"Updated schedule for {job_id}"}

@router.get("/jobs/{job_id}/runs", response_model=List[JobHistory])
async def get_job_runs(job_id: str, scheduler: JobScheduler = Depends(get_scheduler)):
    return scheduler.get_history(job_id)

@router.get("/jobs/{job_id}/runs/{run_id}/logs")
async def get_run_logs(job_id: str, run_id: str, scheduler: JobScheduler = Depends(get_scheduler)):
    logs = scheduler.get_run_logs(run_id)
    if logs is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"logs": logs}
