from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, List
import logging
from arq.connections import RedisSettings
from arq.jobs import Job
from services.coordination.task_queue import TaskQueue

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)

@router.post("/run")
async def run_task(request: Request, mission_data: Dict[str, Any]):
    """Enqueues an agent mission."""
    queue = TaskQueue()
    # Extract details from mission_data
    name = mission_data.get("name", "Unnamed Task")
    agent_id = mission_data.get("agent_id", "Unassigned")
    priority = mission_data.get("priority", "MEDIUM")
    
    task = await queue.submit_task(name, agent_id, priority, mission_data)
    return {"status": "accepted", "job_id": task["id"]}

@router.get("/status")
async def get_queue_status(status: str = None):
    """Returns the list of tasks."""
    queue = TaskQueue()
    tasks = await queue.list_tasks(status)
    return {
        "status": "online",
        "jobs": tasks
    }

@router.post("/kill/{job_id}")
async def kill_job(job_id: str):
    """Aborts a specific job."""
    queue = TaskQueue()
    success = await queue.cancel_task(job_id)
    if not success:
         raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success", "job_id": job_id}

@router.post("/{job_id}/retry")
async def retry_job(job_id: str):
    """Retries a failed/cancelled job."""
    queue = TaskQueue()
    new_task = await queue.retry_task(job_id)
    if not new_task:
         raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "retried", "new_job_id": new_task["id"]}
