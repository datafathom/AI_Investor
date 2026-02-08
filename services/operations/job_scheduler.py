import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class JobScheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JobScheduler, cls).__new__(cls)
            cls._instance.jobs = {}
            cls._instance.history = []
            cls._instance._initialize_mock_jobs()
        return cls._instance

    def _initialize_mock_jobs(self):
        """Initialize some mock jobs for demonstration."""
        self.jobs = {
            "backup_daily": {
                "id": "backup_daily",
                "name": "Daily Database Backup",
                "schedule": "0 0 * * *",
                "last_run": None,
                "status": "idle",
                "type": "system",
                "description": "Full backup of the main PostgreSQL database."
            },
            "data_sync": {
                "id": "data_sync",
                "name": "Market Data Sync",
                "schedule": "*/15 * * * *",
                "last_run": datetime.now().isoformat(),
                "status": "idle",
                "type": "data",
                "description": "Synchronize real-time market data from external providers."
            },
            "model_retrain": {
                "id": "model_retrain",
                "name": "Alpha Model Retraining",
                "schedule": "0 2 * * 0",
                "last_run": (datetime.now().replace(day=datetime.now().day-7)).isoformat(),
                "status": "failed",
                "type": "ml",
                "description": "Retrain Alpha generation models on latest performance data."
            },
            "cache_warm": {
                "id": "cache_warm",
                "name": "Cache Warming",
                "schedule": "*/30 * * * *",
                "last_run": None,
                "status": "idle",
                "type": "system",
                "description": "Pre-load high-frequency data into Redis cache."
            }
        }

    def get_jobs(self) -> List[Dict[str, Any]]:
        return list(self.jobs.values())

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)

    def update_job_schedule(self, job_id: str, schedule: str) -> bool:
        if job_id not in self.jobs:
            return False
        # In a real app, validate cron here
        self.jobs[job_id]["schedule"] = schedule
        logger.info(f"Updated job {job_id} schedule to {schedule}")
        return True

    def get_history(self, job_id: str = None) -> List[Dict[str, Any]]:
        if job_id:
            return [h for h in self.history if h["job_id"] == job_id]
        return self.history

    def get_run_logs(self, run_id: str) -> Optional[str]:
        for run in self.history:
            if run["execution_id"] == run_id:
                return run["logs"]
        return None

    async def trigger_job(self, job_id: str) -> Dict[str, Any]:
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")

        job = self.jobs[job_id]
        job["status"] = "running"
        
        # Simulate execution
        execution_id = f"{job_id}-{int(time.time())}"
        
        # In a real system, this would be a background task
        # For now, we'll simulate a quick async delay
        await asyncio.sleep(1) 
        
        success = True
        if job_id == "model_retrain" and time.time() % 2 == 0: 
            success = False # Simulate intermittent failure for demo

        job["status"] = "idle"
        job["last_run"] = datetime.now().isoformat()
        
        record = {
            "execution_id": execution_id,
            "job_id": job_id,
            "job_name": job["name"],
            "started_at": datetime.now().isoformat(), # approximate
            "ended_at": (datetime.now()).isoformat(),
            "duration_ms": 1200,
            "status": "success" if success else "failed",
            "logs": f"Job {job_id} started at {datetime.now()}...\nProcessing core modules...\nAnalysis of delta set complete.\n" + ("Finalizing commit to production state.\nDone." if success else "CRITICAL ERROR: Data integrity check failed.\nRollback initiated.")
        }
        
        self.history.insert(0, record) # Prepend
        return record

def get_job_scheduler() -> JobScheduler:
    return JobScheduler()
