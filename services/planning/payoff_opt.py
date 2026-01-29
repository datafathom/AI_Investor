"""
Debt Payoff Optimizer.
Calculates Avalanche vs Snowball payoff paths.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DebtOptimizer:
    """Optimizes debt repayment plans."""
    
    def calculate_avalanche(self, debts: List[Dict[str, Any]], extra_payment: float) -> List[str]:
        # Implementation: Sort by interest rate descending
        sorted_debts = sorted(debts, key=lambda x: x['interest_rate'], reverse=True)
        return [f"Pay {d['name']} first (Rate: {d['interest_rate']}%)" for d in sorted_debts]
