import logging
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PowerLawSimulator:
    """
    Simulates Venture Capital portfolio outcomes.
    Models the 'Power Law' where a single deal generates the majority of returns.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PowerLawSimulator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("PowerLawSimulator initialized")

    def simulate_vc_outcomes(self, investment_count: int, ticket_size_k: float = 100) -> Dict[str, Any]:
        """
        Assumptions:
        - 60% fail (0x)
        - 30% mediocre (1-3x)
        - 10% home runs (10-100x)
        """
        total_invested = investment_count * ticket_size_k
        results = []
        
        for _ in range(investment_count):
            roll = random.random()
            if roll < 0.60:
                results.append(0.0)
            elif roll < 0.90:
                results.append(random.uniform(1.0, 3.0) * ticket_size_k)
            else:
                results.append(random.uniform(10.0, 100.0) * ticket_size_k)
                
        total_returned = sum(results)
        fund_multiple = total_returned / total_invested if total_invested > 0 else 0
        
        logger.info(f"VC_LOG: Simulated {investment_count} deals. Fund Multiple: {fund_multiple:.2f}x")
        
        return {
            "total_invested_k": total_invested,
            "total_returned_k": round(total_returned, 2),
            "fund_multiple": round(fund_multiple, 2),
            "winning_ticket_count": len([r for r in results if r > (ticket_size_k * 10)])
        }
