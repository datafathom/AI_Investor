"""
Slippage Estimator Service.
Provides pre-trade estimates of execution costs based on current order book.
"""
from typing import Dict, Any, Optional
import logging
from services.market.depth_aggregator import DepthAggregator

logger = logging.getLogger(__name__)

class SlippageEstimator:
    """
    Calculates expected slippage and market impact.
    """

    @staticmethod
    def estimate_slippage(book: Dict[str, Any], size: float, direction: str) -> Dict[str, float]:
        """
        Estimate slippage for a market order.
        Slippage = (Fill Price - Mid Price) / Mid Price
        
        Args:
            book: Normalized order book.
            size: Order size.
            direction: 'BUY' or 'SELL'.
            
        Returns:
            Dict: {'estimated_vwap': float, 'slippage_pips': float, 'slippage_pct': float}
        """
        mid = book['mid']
        vwap = DepthAggregator.get_vwap_for_size(book, size, direction)
        
        if vwap is None:
            # Cannot fill regular depth
            return {
                'estimated_vwap': 0.0,
                'slippage_pips': 999.0,
                'slippage_pct': 1.0
            }

        # Calculate diff
        diff = abs(vwap - mid)
        symbol = book['symbol']
        pip_size = 0.0001 if not symbol.endswith('JPY') else 0.01
        
        slippage_pips = diff / pip_size
        slippage_pct = diff / mid
        
        return {
            'estimated_vwap': float(vwap),
            'slippage_pips': float(slippage_pips),
            'slippage_pct': float(slippage_pct)
        }
