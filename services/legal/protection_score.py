"""
Asset Protection Scorecard.
Evaluates 'Charging Order Protection' and veil-piercing risk.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ProtectionScorer:
    """Scores entity protection levels."""
    
    def score_entity(self, state: str, has_operating_agreement: bool, multi_member: bool) -> int:
        base_score = 5
        if state in ["NV", "WY"]: base_score += 3
        if has_operating_agreement: base_score += 1
        if multi_member: base_score += 1
        
        return min(10, base_score)
