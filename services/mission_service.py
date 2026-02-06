import json
import os
import uuid
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from config.environment_manager import get_settings
# from web.api.tasks_api import enqueue_job  (We will interact with ARQ directly or via wrapper)

logger = logging.getLogger(__name__)

class MissionService:
    """
    Manages the lifecycle of missions:
    1. Loading templates from Registry.
    2. Configuring mission instance (budget, limits).
    3. Deploying the squad (dispatching jobs to Worker).
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MissionService, cls).__new__(cls)
            cls._instance.templates = []
            cls._instance._load_templates()
        return cls._instance

    def _load_templates(self):
        """Loads mission templates from JSON config."""
        path = os.path.join("config", "mission_templates.json")
        try:
            with open(path, "r") as f:
                self.templates = json.load(f)
            logger.info(f"Loaded {len(self.templates)} mission templates from {path}")
        except Exception as e:
            logger.error(f"Failed to load mission templates: {e}")
            self.templates = []

    def get_all_templates(self, sector: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns filtered list of templates."""
        if sector:
            return [t for t in self.templates if t.get("sector") == sector]
        return self.templates

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        return next((t for t in self.templates if t["id"] == template_id), None)

    async def deploy_mission(self, template_id: str, config: Dict[str, Any], arq_pool) -> Dict[str, Any]:
        """
        Deploys a mission based on a template.
        
        Args:
            template_id: The ID of the template to instantiate.
            config: User-provided overrides (budget_limit, max_steps).
            arq_pool: The ARQ connection pool to enqueue jobs.
            
        Returns:
            Dict containing mission_instance_id and deployed job IDs.
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found.")
            
        mission_id = f"mssn_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Merge defaults with user config
        mission_context = {
            "mission_id": mission_id,
            "template_id": template_id,
            "goal": template["goal"],
            "budget_limit": config.get("budget", template.get("default_budget", 100)),
            "ttl_seconds": config.get("ttl", template.get("default_ttl", 600)),
            "sector": template.get("sector", "General"),
            "risk_level": template.get("risk_level", "Low"),
            "started_at": timestamp
        }
        
        # Identify required departments/agents
        # For simplicity, we assume Dept ID 1 maps to agent 'dept_1_agent' etc.
        # In a real system, we'd use DepartmentRegistry to resolve agents.
        deployed_jobs = []
        
        for dept_id in template.get("required_depts", []):
            # Construct the sub-task for this department
            # This is a simplification. Real logic might divide the goal.
            job_payload = {
                "agent": f"department_{dept_id}_agent", # Naming convention
                "action": "execute_mission_protocol",
                "data": {
                    "mission_context": mission_context,
                    "dept_role": "collaborator"
                }
            }
            
            if arq_pool:
                try:
                    job = await arq_pool.enqueue_job('run_agent_logic', job_payload)
                    deployed_jobs.append(job.job_id)
                    logger.info(f"Deployed Agent {dept_id} for Mission {mission_id} (Job: {job.job_id})")
                except Exception as e:
                    logger.error(f"Failed to enqueue job for Dept {dept_id}: {e}")
            else:
                 logger.warning("ARQ Pool not provided, skipping job enqueue (Simulation Mode)")

        logger.info(f"Mission {mission_id} deployed with {len(deployed_jobs)} agents.")
        
        return {
            "status": "deployed",
            "mission_id": mission_id,
            "jobs": deployed_jobs,
            "context": mission_context
        }

# Singleton
mission_service = MissionService()

def get_mission_service() -> MissionService:
    return mission_service
