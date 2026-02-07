import logging
import asyncio
import shutil
import os
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class BlueGreenService:
    """
    Manages Zero-Downtime deployment of agent logic.
    - GREEN: Production / Live version.
    - BLUE: Staging / New version.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BlueGreenService, cls).__new__(cls)
            cls._instance.active_versions = {} # agent_id -> version_metadata
            cls._instance.backup_root = "backups/agents"
            os.makedirs(cls._instance.backup_root, exist_ok=True)
            
        return cls._instance

    async def deploy_hot_swap(self, agent_id: str, new_code: str, file_path: str) -> Dict[str, Any]:
        """
        Executes a Blue-Green cutover:
        1. Backup Green (current).
        2. Deploy Blue (new).
        3. Verify Blue (Simulation).
        4. Cutover: Promote Blue to Green.
        """
        deployment_id = f"dep_{uuid.uuid4().hex[:6]}"
        logger.info(f"[{deployment_id}] Swapping logic for {agent_id}...")
        
        # 1. Backup Green
        backup_path = None
        if os.path.exists(file_path):
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.backup_root, agent_id)
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f"green_{timestamp}.py")
            shutil.copy(file_path, backup_path)
            logger.info(f"[{deployment_id}] Green backup: {backup_path}")

        # 2. Deploy Blue (to staging or direct overwrite for simple prototype)
        # In real system: Deploy to a /staging/ directory first.
        # For prototype: Direct overwrite with verification.
        try:
            with open(file_path, "w") as f:
                f.write(new_code)
            
            # 3. Verify Blue
            logger.info(f"[{deployment_id}] Verifying Blue version...")
            await asyncio.sleep(1.0) # Simulating static analysis/startup
            
            # 4. Cutover
            version_meta = {
                "deployment_id": deployment_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "backup": backup_path,
                "status": "LIVE"
            }
            self.active_versions[agent_id] = version_meta
            
            logger.info(f"[{deployment_id}] Cutover SUCCESSFUL. {agent_id} is now on BLUE version.")
            return {"status": "success", "deployment_id": deployment_id, "meta": version_meta}
            
        except Exception as e:
            logger.error(f"[{deployment_id}] Deployment FAILED: {e}")
            if backup_path:
                logger.info(f"[{deployment_id}] Rolling back to Green...")
                shutil.copy(backup_path, file_path)
            return {"status": "failed", "error": str(e)}

    def rollback(self, agent_id: str, file_path: str) -> bool:
        """
        Restores most recent Green backup.
        """
        meta = self.active_versions.get(agent_id)
        if not meta or not meta.get("backup"):
            logger.error(f"No valid backup found for {agent_id}")
            return False
            
        try:
            shutil.copy(meta["backup"], file_path)
            logger.info(f"Rollback for {agent_id} SUCCESSFUL.")
            self.active_versions[agent_id]["status"] = "ROLLED_BACK"
            return True
        except Exception as e:
            logger.error(f"Critical error during rollback for {agent_id}: {e}")
            return False

# Singleton
blue_green_service = BlueGreenService()
def get_blue_green_service() -> BlueGreenService:
    return blue_green_service
