import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

WORKSPACES_FILE = "workspaces_data.json"

class WorkspaceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkspaceManager, cls).__new__(cls)
            cls._instance.file_path = WORKSPACES_FILE
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        if not os.path.exists(self.file_path):
            self.workspaces = self._get_default_workspaces()
            self._save_data()
        else:
            try:
                with open(self.file_path, 'r') as f:
                    self.workspaces = json.load(f)
            except json.JSONDecodeError:
                self.workspaces = self._get_default_workspaces()

    def _get_default_workspaces(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "ws-prod-main",
                "user_id": "admin",
                "name": "Production Main",
                "layout": {"type": "default"},
                "users": [
                    {"user_id": "admin", "role": "admin"},
                    {"user_id": "trader-1", "role": "editor"}
                ],
                "quotas": {
                    "storage_gb": 100,
                    "api_calls_day": 50000,
                    "concurrent_sessions": 10
                },
                "usage": {
                    "storage_gb": 42.5,
                    "api_calls_today": 12450
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": "ws-devlink",
                "user_id": "admin",
                "name": "Development Sandbox",
                "layout": {"type": "grid"},
                "users": [
                    {"user_id": "admin", "role": "admin"},
                    {"user_id": "dev-user", "role": "admin"}
                ],
                "quotas": {
                    "storage_gb": 10,
                    "api_calls_day": 5000,
                    "concurrent_sessions": 2
                },
                "usage": {
                    "storage_gb": 0.5,
                    "api_calls_today": 120
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]

    def _save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.workspaces, f, indent=2)

    def list_workspaces(self) -> List[Dict[str, Any]]:
        self._load_data() # Refresh in case of external edits
        return self.workspaces

    def create_workspace(self, name: str, layout: Dict[str, Any], user_id: str = "admin") -> Dict[str, Any]:
        new_workspace = {
            "id": f"ws-{str(uuid.uuid4())[:8]}",
            "user_id": user_id,
            "name": name,
            "layout": layout,
            "users": [{"user_id": user_id, "role": "admin"}],
            "quotas": {
                "storage_gb": 10,
                "api_calls_day": 1000,
                "concurrent_sessions": 1
            },
            "usage": {
                "storage_gb": 0,
                "api_calls_today": 0
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.workspaces.append(new_workspace)
        self._save_data()
        logger.info(f"Created workspace: {name}")
        return new_workspace

    def get_workspace(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        return next((w for w in self.workspaces if w["id"] == workspace_id), None)

    def assign_user(self, workspace_id: str, user_id: str, role: str) -> bool:
        ws = self.get_workspace(workspace_id)
        if not ws: return False
        
        # Remove if already exists
        ws["users"] = [u for u in ws["users"] if u["user_id"] != user_id]
        ws["users"].append({"user_id": user_id, "role": role})
        
        ws["updated_at"] = datetime.now().isoformat()
        self._save_data()
        return True

    def remove_user(self, workspace_id: str, user_id: str) -> bool:
        ws = self.get_workspace(workspace_id)
        if not ws: return False
        
        ws["users"] = [u for u in ws["users"] if u["user_id"] != user_id]
        ws["updated_at"] = datetime.now().isoformat()
        self._save_data()
        return True

    def update_quotas(self, workspace_id: str, quotas: Dict[str, Any]) -> bool:
        ws = self.get_workspace(workspace_id)
        if not ws: return False
        
        ws["quotas"].update(quotas)
        ws["updated_at"] = datetime.now().isoformat()
        self._save_data()
        return True

    def update_workspace(self, workspace_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return None
        
        workspace.update(updates)
        workspace["updated_at"] = datetime.now().isoformat()
        self._save_data()
        logger.info(f"Updated workspace: {workspace['name']}")
        return workspace

    def delete_workspace(self, workspace_id: str) -> bool:
        initial_len = len(self.workspaces)
        self.workspaces = [w for w in self.workspaces if w["id"] != workspace_id]
        if len(self.workspaces) < initial_len:
            self._save_data()
            logger.info(f"Deleted workspace: {workspace_id}")
            return True
        return False

def get_workspace_manager() -> WorkspaceManager:
    return WorkspaceManager()
