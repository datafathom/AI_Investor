"""
Stock Donation Optimizer.
Identifies best lots for DAF contributions.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DonationOptimizer:
    """Finds high-appreciation lots for tax-efficient giving."""
    
    def find_best_donations(self, holdings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Sort by % gain descending
        sorted_lots = sorted(holdings, key=lambda x: (x['current_price'] - x['cost_basis']) / x['cost_basis'], reverse=True)
        
        return [{
            "ticker": l['ticker'],
            "gain_pct": round((l['current_price'] - l['cost_basis']) / l['cost_basis'] * 100, 2),
            "tax_saved": (l['current_price'] - l['cost_basis']) * 0.20 # Est cap gains rate
        } for l in sorted_lots[:3]]
