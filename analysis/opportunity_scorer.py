"""
Opportunity Scorer Module.
Scores identified patterns based on confluence.
"""
from typing import Dict

class OpportunityScorer:
    @staticmethod
    def score_opportunity(pattern: Dict) -> float:
        """
        Score an opportunity from 0 to 100.
        """
        base_score = 50.0
        
        # Boost for confidence
        confidence = pattern.get("confidence", 0.0)
        base_score += (confidence * 30) # Max +30
        
        # Boost for specific patterns (example)
        if "Engulfing" in pattern.get("pattern", ""):
            base_score += 10
            
        return min(base_score, 100.0)
