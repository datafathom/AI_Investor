"""
==============================================================================
FILE: services/strategy/tax_harvester.py
ROLE: Tax Optimization Engine
PURPOSE:
    Identify opportunities to harvest tax losses while avoiding Wash Sales.
    
    Logic:
    - Harvesting:
        - If Unrealized Loss < -5% OR Raw Loss > $500: Candidate for Harvest.
    - Wash Sale Avoidance:
        - If Symbol was sold for a loss in the last 30 days, DO NOT BUY back.
        - (Advanced: If selling now, ensure we don't buy back for 30 days).
        
ROADMAP: Phase 19 - Tax-Efficiency
==============================================================================
"""

import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TaxHarvester:
    def __init__(self):
        # Thresholds
        self.LOSS_PCT_THRESHOLD = -0.05  # -5%
        self.RAW_LOSS_THRESHOLD = 500.0  # $500
        self.WASH_SALE_WINDOW = 30 # Days

    def scan_harvestable_losses(self, 
                              positions: List[Dict[str, Any]], 
                              current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Scan open positions for harvesting candidates.
        
        Args:
            positions: List of dicts {'symbol': 'AAPL', 'quantity': 10, 'cost_basis_per_share': 150.0}
            current_prices: Dict {'AAPL': 140.0}
            
        Returns:
            List of recommendations: [{'symbol': 'AAPL', 'action': 'HARVEST', 'reason': 'Loss > 5%'}]
        """
        recommendations = []
        
        for pos in positions:
            symbol = pos['symbol']
            qty = pos['quantity']
            cost = pos['cost_basis_per_share']
            
            if symbol not in current_prices:
                continue
                
            price = current_prices[symbol]
            current_val = price * qty
            cost_val = cost * qty
            
            raw_gain_loss = current_val - cost_val
            pct_gain_loss = raw_gain_loss / cost_val if cost_val > 0 else 0.0
            
            # Check Harvesting Criteria
            if raw_gain_loss < 0:
                is_harvestable = False
                reason = ""
                
                if pct_gain_loss < self.LOSS_PCT_THRESHOLD:
                    is_harvestable = True
                    reason = f"Loss {pct_gain_loss*100:.1f}% exceeds threshold {self.LOSS_PCT_THRESHOLD*100}%"
                    
                elif abs(raw_gain_loss) > self.RAW_LOSS_THRESHOLD:
                    is_harvestable = True
                    reason = f"Raw Loss ${abs(raw_gain_loss):.2f} exceeds threshold ${self.RAW_LOSS_THRESHOLD}"
                    
                if is_harvestable:
                    recommendations.append({
                        'symbol': symbol,
                        'action': 'HARVEST',
                        'estimated_loss': raw_gain_loss,
                        'reason': reason
                    })
                    
        return recommendations

    def check_wash_sale_restriction(self, 
                                  symbol: str, 
                                  transaction_history: List[Dict[str, Any]], 
                                  current_date: Optional[datetime] = None) -> bool:
        """
        Check if 'symbol' is restricted from being BOUGHT due to a Wash Sale rule.
        (i.e., was sold for a loss within the last 30 days).
        
        Args:
            transaction_history: List of {'symbol', 'action', 'date', 'pnl'}
        """
        if current_date is None:
            current_date = datetime.now()
            
        cutoff_date = current_date - timedelta(days=self.WASH_SALE_WINDOW)
        
        for txn in transaction_history:
            if txn['symbol'] == symbol and txn['action'] == 'SELL':
                txn_date = txn['date']
                if isinstance(txn_date, str):
                    try:
                        txn_date = datetime.fromisoformat(txn_date)
                    except ValueError:
                        continue # Skip invalid dates
                        
                # If sold for a loss RECENTLY
                if txn_date >= cutoff_date:
                    if txn.get('pnl', 0) < 0:
                        return True # Restricted
                        
        return False

# Singleton
_instance = None

def get_tax_harvester() -> TaxHarvester:
    global _instance
    if _instance is None:
        _instance = TaxHarvester()
    return _instance
