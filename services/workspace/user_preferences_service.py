
"""User workspace and preferences management."""
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from utils.database_manager import get_database_manager

logger = logging.getLogger(__name__)

class WindowState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    title: str
    x: int
    y: int
    width: int
    height: int
    z_index: int = Field(alias="zIndex", default=0)
    is_minimized: bool = Field(alias="isMinimized", default=False)
    is_maximized: bool = Field(alias="isMaximized", default=False)

class WorkspaceLayout(BaseModel):
    workspace_id: Optional[str] = None
    workspace_name: str
    windows: List[WindowState]
    saved_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UserPreferencesService:
    """Manages user workspace layouts in Postgres."""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserPreferencesService, cls).__new__(cls)
            cls._instance.db = get_database_manager()
        return cls._instance

    def save_workspace(self, user_id: str, workspace: WorkspaceLayout, is_default: bool = False) -> str:
        """
        Save workspace layout with <200ms target.
        Returns the workspace ID.
        """
        layout_json = json.dumps([w.model_dump(by_alias=True) for w in workspace.windows])
        
        with self.db.pg_cursor() as cur:
            cur.execute("""
                INSERT INTO user_workspaces (user_id, workspace_name, layout_json, is_default, updated_at)
                VALUES (%s, %s, %s, %s, NOW())
                ON CONFLICT (user_id, workspace_name) 
                DO UPDATE SET 
                    layout_json = EXCLUDED.layout_json,
                    is_default = EXCLUDED.is_default,
                    updated_at = NOW()
                RETURNING id
            """, (user_id, workspace.workspace_name, layout_json, is_default))
            
            res = cur.fetchone()
            return str(res[0])
    
    def get_workspace(self, user_id: str, workspace_name: str = None) -> Optional[WorkspaceLayout]:
        """Retrieve workspace by name, or default if None."""
        with self.db.pg_cursor() as cur:
            if workspace_name:
                cur.execute("""
                    SELECT id, workspace_name, layout_json, updated_at 
                    FROM user_workspaces 
                    WHERE user_id = %s AND workspace_name = %s
                """, (user_id, workspace_name))
            else:
                cur.execute("""
                    SELECT id, workspace_name, layout_json, updated_at 
                    FROM user_workspaces 
                    WHERE user_id = %s AND is_default = true 
                    LIMIT 1
                """, (user_id,))
                
            row = cur.fetchone()
            if not row:
                return None
                
            windows_data = json.loads(row[2]) if isinstance(row[2], str) else row[2]
            windows = [WindowState(**w) for w in windows_data]
                
            return WorkspaceLayout(
                workspace_id=str(row[0]),
                workspace_name=row[1],
                windows=windows,
                saved_at=row[3]
            )
    
    def list_workspaces(self, user_id: str) -> List[Dict[str, Any]]:
        """List all saved workspaces for user."""
        with self.db.pg_cursor() as cur:
            cur.execute("""
                SELECT id, workspace_name, is_default, updated_at 
                FROM user_workspaces 
                WHERE user_id = %s 
                ORDER BY updated_at DESC
            """, (user_id,))
            
            return [
                {
                    "id": str(r[0]),
                    "name": r[1],
                    "is_default": r[2],
                    "last_modified": r[3].isoformat() if r[3] else None
                }
                for r in cur.fetchall()
            ]
    
    def delete_workspace(self, user_id: str, workspace_name: str) -> bool:
        """Delete a saved workspace."""
        with self.db.pg_cursor() as cur:
            cur.execute("""
                DELETE FROM user_workspaces 
                WHERE user_id = %s AND workspace_name = %s
            """, (user_id, workspace_name))
            return cur.rowcount > 0

def get_user_preferences_service() -> UserPreferencesService:
    return UserPreferencesService()
