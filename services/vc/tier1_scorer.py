import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Tier1Scorer:
    """
    Phase 165.2: Top 8 VC Firm Access Table.
    Scores VC firms based on historical MOIC and network density.
    """
    
    @staticmethod
    def get_firm_score(firm_name: str) -> Dict[str, Any]:
        """
        Heuristic scores for top-tier firms.
        """
        top_firms = {
            "SEQUOIA": 9.8,
            "A16Z": 9.5,
            "BENCHMARK": 9.9,
            "FOUNDERS_FUND": 9.7,
            "ACCEL": 9.4,
            "KLEINER_PERKINS": 9.2,
            "GREYLOCK": 9.3,
            "LIGHTSPEED": 9.1
        }
        
        score = top_firms.get(firm_name.upper(), 5.0)
        is_tier1 = score >= 9.0
        
        logger.info(f"VC_LOG: Firm {firm_name} score: {score} (Tier 1: {is_tier1})")
        return {
            "firm": firm_name.upper(),
            "prestige_score": score,
            "is_tier1": is_tier1,
            "access_difficulty": "EXTREME" if is_tier1 else "MODERATE"
        }
