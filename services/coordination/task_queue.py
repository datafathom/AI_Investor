import logging
import asyncio
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskQueue:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskQueue, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.tasks: Dict[str, Dict] = {}
        self._generate_mock_tasks()
        self._initialized = True

    def _generate_mock_tasks(self):
        """Generate mock tasks for UI development."""
        tasks = [
            {"name": "Market Scan", "agent": "AGENT-042", "priority": "HIGH"},
            {"name": "Portfolio Rebalance", "agent": "AGENT-007", "priority": "CRITICAL"},
            {"name": "Sentiment Analysis", "agent": "AGENT-013", "priority": "MEDIUM"},
            {"name": "Data Ingestion", "agent": "AGENT-099", "priority": "LOW"},
            {"name": "Risk Audit", "agent": "AGENT-001", "priority": "HIGH"},
        ]
        
        for t in tasks:
            task_id = str(uuid.uuid4())
            self.tasks[task_id] = {
                "id": task_id,
                "name": t["name"],
                "assigned_agent": t["agent"],
                "priority": t["priority"],
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "started_at": None,
                "completed_at": None,
                "inputs": {"target": "SPY", "depth": "full"},
                "outputs": None
            }

    async def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """List all tasks, optionally filtered by status."""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t["status"].lower() == status.lower()]
        return sorted(tasks, key=lambda x: x["created_at"], reverse=True)

    async def get_task(self, task_id: str) -> Optional[Dict]:
        return self.tasks.get(task_id)

    async def submit_task(self, name: str, agent_id: str, priority: str = "MEDIUM", inputs: Dict = {}) -> Dict:
        """Submit a new task."""
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "name": name,
            "assigned_agent": agent_id,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "inputs": inputs,
            "outputs": None
        }
        self.tasks[task_id] = task
        # In real implementation, enqueue to Redis/ARQ here
        return task

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "cancelled"
            self.tasks[task_id]["completed_at"] = datetime.now().isoformat()
            return True
        return False
    
    async def retry_task(self, task_id: str) -> Optional[Dict]:
        """Retry a failed task."""
        if task_id in self.tasks:
            old_task = self.tasks[task_id]
            # Create new task as clone
            return await self.submit_task(
                name=old_task["name"],
                agent_id=old_task["assigned_agent"],
                priority=old_task["priority"],
                inputs=old_task["inputs"]
            )
        return None
