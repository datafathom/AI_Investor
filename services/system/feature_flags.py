import os
import json
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

FLAGS_FILE = "feature_flags.json"

DEFAULT_FLAGS = {
    "DARK_MODE": {
        "enabled": True,
        "percentage": 100,
        "targeting": [],
        "description": "Global dark mode theme toggle."
    },
    "BETA_TRADING_ALGO": {
        "enabled": False,
        "percentage": 10,
        "targeting": [{"attribute": "user_id", "operator": "in", "values": ["admin", "beta-tester"]}],
        "description": "Next-gen Alpha Signal generation algorithm."
    },
    "NEW_DASHBOARD_LAYOUT": {
        "enabled": False,
        "percentage": 50,
        "targeting": [],
        "description": "Refactored high-fidelity Mission Control layout."
    },
    "MAINTENANCE_MODE": {
        "enabled": False,
        "percentage": 0,
        "targeting": [{"attribute": "user_id", "operator": "not_in", "values": ["admin"]}],
        "description": "Restricts access during system upgrades."
    },
    "DEBUG_LOGGING": {
        "enabled": False,
        "percentage": 0,
        "targeting": [],
        "description": "Enable verbose trace logs for all system components."
    }
}

class FeatureFlagManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FeatureFlagManager, cls).__new__(cls)
            cls._instance._load_flags()
        return cls._instance

    def _load_flags(self):
        self.file_path = Path(FLAGS_FILE)
        if not self.file_path.exists():
            self.flags = DEFAULT_FLAGS.copy()
            self._save_flags()
        else:
            try:
                with open(self.file_path, 'r') as f:
                    self.flags = json.load(f)
                
                # Migration/Merge
                updated = False
                for key, val in DEFAULT_FLAGS.items():
                    if key not in self.flags:
                        self.flags[key] = val
                        updated = True
                    elif isinstance(self.flags[key], bool):
                        # Migrate legacy boolean flags
                        self.flags[key] = {
                            "enabled": self.flags[key],
                            "percentage": 100 if self.flags[key] else 0,
                            "targeting": [],
                            "description": val["description"]
                        }
                        updated = True
                
                if updated:
                    self._save_flags()
            except Exception as e:
                logger.error(f"Failed to load feature flags: {e}")
                self.flags = DEFAULT_FLAGS.copy()

    def _save_flags(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.flags, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save feature flags: {e}")

    def get_all_flags(self) -> Dict[str, Any]:
        return self.flags

    def evaluate_flag(self, name: str, context: Dict[str, Any]) -> bool:
        flag = self.flags.get(name)
        if not flag: return False
        if not flag.get("enabled", False): return False
        
        # 1. Evaluate Targeting Rules
        targeting = flag.get("targeting", [])
        if targeting:
            for rule in targeting:
                attr = rule.get("attribute")
                op = rule.get("operator")
                vals = rule.get("values", [])
                
                ctx_val = context.get(attr)
                if op == "in" and ctx_val not in vals: return False
                if op == "not_in" and ctx_val in vals: return False
                # Add more operators as needed

        # 2. Evaluate Percentage
        percentage = flag.get("percentage", 100)
        if percentage < 100:
            # Deterministic hash of user_id (if present) or random
            user_id = context.get("user_id", "")
            if user_id:
                # Basic bucketizing
                bucket = sum(ord(c) for c in user_id) % 100
                if bucket >= percentage: return False
            elif percentage == 0:
                return False

        return True

    def update_flag(self, name: str, updates: Dict[str, Any]) -> bool:
        if name not in self.flags:
            # For demo, allow creating new ones
            self.flags[name] = {
                "enabled": False,
                "percentage": 0,
                "targeting": [],
                "description": ""
            }
        
        self.flags[name].update(updates)
        self._save_flags()
        logger.info(f"Updated feature flag: {name}")
        return True

    def toggle_flag(self, name: str) -> bool:
        if name in self.flags:
            self.flags[name]["enabled"] = not self.flags[name]["enabled"]
            self._save_flags()
            return True
        return False

def get_feature_flag_manager() -> FeatureFlagManager:
    return FeatureFlagManager()
