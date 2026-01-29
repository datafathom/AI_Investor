"""
Net Liquidity Calculator.
Formula: Fed Balance Sheet - TGA - RRP.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NetLiquidityCalc:
    """Calculates effective market liquidity."""
    
    def calculate_net(self, fed_assets: float, tga_balance: float, rrp_usage: float) -> float:
        net_liq = fed_assets - tga_balance - rrp_usage
        logger.info(f"LIQUIDITY_LOG: Net Liquidity calculated at ${net_liq/1e12:.2f}T")
        return net_liq
