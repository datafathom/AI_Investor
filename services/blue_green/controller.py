import logging
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

STATE_FILE = "blue_green_state.json"

class BlueGreenController:
    """
    Manages Blue/Green deployment state, traffic splitting, and rollbacks.
    Persists state to a local file for now.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BlueGreenController, cls).__new__(cls)
            cls._instance._load_state()
        return cls._instance

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    self.state = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load blue/green state: {e}")
                self._reset_default_state()
        else:
            self._reset_default_state()

    def _reset_default_state(self):
        self.state = {
            "active_env": "blue",  # 'blue' or 'green'
            "traffic_split": {
                "blue": 100,
                "green": 0
            },
            "environments": {
                "blue": {
                    "version": "v1.0.0",
                    "status": "healthy",
                    "last_deployed": datetime.now().isoformat()
                },
                "green": {
                    "version": "v1.1.0-rc1",
                    "status": "idle",
                    "last_deployed": datetime.now().isoformat()
                }
            },
            "history": []
        }
        self._save_state()

    def _save_state(self):
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save blue/green state: {e}")

    def get_status(self) -> Dict[str, Any]:
        return self.state

    def switch_environment(self, target_env: str) -> Dict[str, Any]:
        if target_env not in ["blue", "green"]:
            raise ValueError("Invalid environment. Must be 'blue' or 'green'.")

        previous_env = self.state["active_env"]
        
        # 1. Update Active Env
        self.state["active_env"] = target_env
        
        # 2. Update Traffic (100% to target)
        self.state["traffic_split"] = {
            "blue": 100 if target_env == "blue" else 0,
            "green": 100 if target_env == "green" else 0
        }
        
        # 3. Update Statuses
        self.state["environments"][target_env]["status"] = "active"
        self.state["environments"][previous_env]["status"] = "idle"

        # 4. Record History
        self.state["history"].insert(0, {
            "action": "switch",
            "from": previous_env,
            "to": target_env,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_state()
        logger.info(f"Switched environment to {target_env}")
        return self.state

    def set_traffic_split(self, blue_pct: int, green_pct: int) -> Dict[str, Any]:
        if blue_pct + green_pct != 100:
            raise ValueError("Traffic split must check up to 100%.")
        
        self.state["traffic_split"] = {
            "blue": blue_pct,
            "green": green_pct
        }
        
        # Update active env based on majority rule logic for now, 
        # or keep explicit active_env as the "primary" one.
        # We'll keep active_env unchanged unless explicit switch is called, 
        # but traffic can be split.
        
        self.state["history"].insert(0, {
            "action": "traffic_update",
            "split": {"blue": blue_pct, "green": green_pct},
            "timestamp": datetime.now().isoformat()
        })

        self._save_state()
        logger.info(f"Updated traffic split: Blue {blue_pct}% / Green {green_pct}%")
        return self.state

    def rollback(self) -> Dict[str, Any]:
        # Simple rollback: just switch to the OTHER environment
        current = self.state["active_env"]
        target = "green" if current == "blue" else "blue"
        
        logger.warning(f"Rolling back from {current} to {target}")
        result = self.switch_environment(target)
        
        # Mark rollback in history
        self.state["history"][0]["action"] = "rollback" # Override the 'switch' action label
        self._save_state()
        
        return result

def get_blue_green_controller() -> BlueGreenController:
    return BlueGreenController()
