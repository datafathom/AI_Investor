import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import dotenv_values, set_key

logger = logging.getLogger(__name__)

ENV_FILE = ".env"
HISTORY_FILE = "config/env_history.json"
SENSITIVE_KEYS = [
    "API_KEY", "SECRET", "PASSWORD", "TOKEN", "KEY", "CREDENTIALS", 
    "PRIVATE", "AUTH", "OPENAI_API_KEY", "SLACK_BOT_TOKEN", "SLACK_APP_TOKEN"
]

class EnvManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.history = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def _log_history(self, action: str, key: str, value: str = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "key": key,
            "user": "admin" # Mock user
        }
        self.history.insert(0, entry)
        self.history = self.history[:50] # Keep last 50
        
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_all_vars(self) -> List[Dict[str, Any]]:
        """
        Returns a list of environment variables with metadata.
        """
        if os.path.exists(ENV_FILE):
            env_vars = dotenv_values(ENV_FILE)
        else:
            env_vars = dict(os.environ)

        result = []
        for key, value in env_vars.items():
            is_sensitive = any(s in key.upper() for s in SENSITIVE_KEYS)
            masked_value = "******" if is_sensitive and value else value
            result.append({
                "key": key,
                "value": masked_value,
                "is_sensitive": is_sensitive,
                "updated_at": next((h["timestamp"] for h in self.history if h["key"] == key), "Unknown")
            })
        
        return sorted(result, key=lambda x: x["key"])

    def update_var(self, key: str, value: str) -> bool:
        try:
            if not os.path.exists(ENV_FILE):
                with open(ENV_FILE, 'w') as f:
                    f.write(f"{key}={value}\n")
            else:
                set_key(ENV_FILE, key, value)
            
            os.environ[key] = value
            self._log_history("update", key)
            logger.info(f"Updated environment variable: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to update environment variable {key}: {e}")
            return False

    def bulk_update_vars(self, updates: Dict[str, str]) -> bool:
        success = True
        for key, value in updates.items():
            if not self.update_var(key, value):
                success = False
        return success

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

def get_env_manager() -> EnvManager:
    return EnvManager()
