"""
Triple Confluence Signal Engine.
Requires agreement from Technicals, Macro, and Fundamentals.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TripleConfluenceEngine:
    """Calculates the absolute signal score (0-100)."""
    
    def calculate_score(self, tech_score: int, fund_score: int, macro_score: int) -> Dict[str, Any]:
        avg = (tech_score + fund_score + macro_score) / 3
        
        # Weighted toward Macro in conflict
        is_valid = tech_score > 70 and fund_score > 70 and macro_score > 50
        
        return {
            "total_score": round(avg, 2),
            "is_valid_signal": is_valid,
            "reason": "Triple alignment" if is_valid else "Lack of alignment"
        }
