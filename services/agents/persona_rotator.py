"""
Agent Persona Rotator - Phase 33.
Dynamically switches agent personas based on market conditions.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PersonaRotator:
    """Rotates agent personas based on market regime."""
    
    PERSONAS = ["SEARCHER", "STACKER", "WARDEN", "PROTECTOR"]
    
    @staticmethod
    def get_optimal_persona(market_regime: str) -> str:
        if market_regime == "TRENDING":
            return "SEARCHER"
        elif market_regime == "RANGING":
            return "STACKER"
        elif market_regime == "HIGH_VOL":
            return "PROTECTOR"
        return "WARDEN"
