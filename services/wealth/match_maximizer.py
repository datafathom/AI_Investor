"""
401k Employer Match Maximizer - Phase 47.
Optimizes contributions to maximize employer match.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MatchMaximizer:
    """Maximizes 401k employer match."""
    
    @staticmethod
    def calculate_optimal_contribution(
        salary: float,
        match_pct: float,
        match_cap_pct: float
    ) -> Dict[str, float]:
        # Employer matches match_pct up to match_cap_pct of salary
        max_match = salary * match_cap_pct * match_pct
        required_contribution = salary * match_cap_pct
        
        return {
            "min_contribution_for_full_match": required_contribution,
            "max_employer_match": max_match,
            "effective_return": match_pct * 100
        }
