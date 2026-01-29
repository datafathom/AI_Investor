import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AccumulationProjector:
    """Projects retirement account growth over 40 years."""
    
    def project_growth(self, starting_balance: float, annual_contrib: float, growth_rate: float, years: int) -> List[Dict[str, Any]]:
        history = []
        balance = starting_balance
        
        for year in range(1, years + 1):
            growth = balance * growth_rate
            balance += growth + annual_contrib
            history.append({
                "year": year,
                "growth": round(growth, 2),
                "contribution": annual_contrib,
                "ending_balance": round(balance, 2)
            })
            
        logger.info(f"PROJECTOR_LOG: Projected growth to ${balance:,.2f} over {years} years.")
        return history
