"""
Mode Controller Service
Manages system operating modes (Defense, Attack, Stealth, Zen).
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ModeController:
    _instance = None
    
    MODES = {
        "DEFENSE": {
            "description": "Capital preservation, high alerts, conservative trading.",
            "risk_multiplier": 0.5,
            "theme": "defense"
        },
        "ATTACK": {
            "description": "Aggressive growth, opportunistic, high leverage.",
            "risk_multiplier": 1.5,
            "theme": "attack"
        },
        "STEALTH": {
            "description": "Low profile, minimal logging, hidden operations.",
            "risk_multiplier": 1.0,
            "theme": "stealth"
        },
        "ZEN": {
            "description": "Balanced, homeostasis, long-term focus.",
            "risk_multiplier": 0.8,
            "theme": "zen"
        }
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModeController, cls).__new__(cls)
            cls._instance._current_mode = "ZEN"
            cls._instance._mode_history = []
    
    def get_current_mode(self) -> Dict:
        return {
            "mode": self._current_mode,
            "details": self.MODES[self._current_mode]
        }

    def list_modes(self) -> Dict:
        return self.MODES

    def switch_mode(self, mode: str) -> Dict:
        mode = mode.upper()
        if mode not in self.MODES:
            raise ValueError(f"Invalid mode: {mode}")
        
        previous_mode = self._current_mode
        self._current_mode = mode
        
        # Log transition
        from datetime import datetime
        entry = {
            "timestamp": datetime.now().isoformat(),
            "from": previous_mode,
            "to": mode,
            "reason": "Manual Switch"
        }
        self._mode_history.insert(0, entry) # Keep recent first
        self._mode_history = self._mode_history[:50] # Keep last 50
        
        logger.info(f"System mode switched from {previous_mode} to {mode}")
        return self.get_current_mode()

    def get_history(self) -> List[Dict]:
        return self._mode_history

def get_mode_controller():
    return ModeController()
