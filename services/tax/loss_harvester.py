
import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LossHarvester:
    """
    Identifies 'Loser' tax lots to offset acknowledged gains.
    Aims for Net Zero taxable gain.
    """
    
    def find_offset_candidates(self, recognized_gains: Decimal, portfolio_lots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Matches gains with unrealized losses.
        """
        logger.info(f"Targeting ${recognized_gains} in offsets.")
        
        # Heuristic: Sort by greatest unrealized loss percentage
        losers = [lot for lot in portfolio_lots if lot["unrealized_gain_loss"] < 0]
        losers.sort(key=lambda x: x["unrealized_gain_loss"])
        
        candidates = []
        covered_gain = Decimal('0.00')
        
        for lot in losers:
            if covered_gain >= recognized_gains:
                break
            
            loss = Decimal(str(abs(lot["unrealized_gain_loss"])))
            candidates.append(lot)
            covered_gain += loss
            
        logger.info(f"Loss Harvesting: Found {len(candidates)} lots to offset ${covered_gain}")
        
        return candidates
