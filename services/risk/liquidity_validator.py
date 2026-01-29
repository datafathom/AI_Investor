"""
Liquidity Validator Service.
Enforces execution safety gates based on real-time depth data.
"""
import logging
from typing import Dict, Any, Optional
from config.liquidity_thresholds import get_asset_standards
from services.market.depth_aggregator import DepthAggregator

logger = logging.getLogger(__name__)

class LiquidityValidator:
    """
    Validates if a symbol and order size are safe for execution.
    """

    @staticmethod
    def is_safe_to_execute(book: Dict[str, Any], order_size: Optional[float] = None) -> Dict[str, Any]:
        """
        Check spread and depth against predefined standards.
        
        Returns:
            Dict: {'safe': bool, 'reason': str, 'metrics': dict}
        """
        symbol = book['symbol']
        standards = get_asset_standards(symbol)
        
        # 1. Check Spread
        # Convert raw spread to pips (assuming 4th decimal for simplicity or getting pip size from config)
        # For MAJOR_FX, 0.0001 = 1 pip.
        raw_spread = book['spread']
        pip_size = 0.0001 if not symbol.endswith('JPY') else 0.01
        spread_pips = raw_spread / pip_size if raw_spread else 999.0
        
        spread_ok = spread_pips <= standards['max_spread_pips']
        
        # 2. Check Depth (Volume within 5 pips)
        metrics = DepthAggregator.get_total_volume_at_depth(book, pip_range=5 * pip_size)
        total_depth = metrics['bid_volume'] + metrics['ask_volume']
        depth_ok = total_depth >= standards['min_depth']
        
        # 3. Size-specific check (Optional)
        # If we have an order size, ensure we can fill it within a reasonable price range
        size_ok = True
        if order_size:
            # We assume we need to fill the size on one side (e.g. buying needs ask depth)
            size_ok = (metrics['ask_volume'] >= order_size) # Very simple check
            
        safe = spread_ok and depth_ok and size_ok
        
        reason = "OK"
        if not safe:
            res_list = []
            if not spread_ok: res_list.append(f"High Spread ({spread_pips:.1f} pips)")
            if not depth_ok: res_list.append(f"Thin Depth ({total_depth:.0f})")
            if not size_ok: res_list.append("Insufficient Volume for size")
            reason = " | ".join(res_list)

        return {
            'safe': safe,
            'reason': reason,
            'metrics': {
                'spread_pips': spread_pips,
                'total_depth': total_depth,
                'imbalance': metrics['imbalance']
            }
        }
