"""
Performance Attribution Logic.
Analyzes sources of return (Asset Allocation vs. Selection).
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PerformanceAttribution:
    """Brinson-Fachler attribution model (simplified)."""
    
    def calculate_attribution(self, portfolio_return: float, benchmark_return: float, 
                            sector_weights_port: Dict[str, float], sector_weights_bench: Dict[str, float],
                            sector_returns_port: Dict[str, float], sector_returns_bench: Dict[str, float]) -> Dict[str, float]:
                            
        allocation_effect = 0.0
        selection_effect = 0.0
        
        for sector in sector_weights_bench.keys():
            wp = sector_weights_port.get(sector, 0)
            wb = sector_weights_bench.get(sector, 0)
            rp = sector_returns_port.get(sector, 0)
            rb = sector_returns_bench.get(sector, 0)
            
            # Allocation: Did we overweight a winning sector?
            allocation_effect += (wp - wb) * (rb - benchmark_return)
            
            # Selection: Did we pick winning stocks in that sector?
            selection_effect += wb * (rp - rb)
            
        interaction = portfolio_return - benchmark_return - allocation_effect - selection_effect
        
        return {
            "total_alpha": portfolio_return - benchmark_return,
            "allocation_effect": allocation_effect,
            "selection_effect": selection_effect,
            "interaction_effect": interaction
        }
