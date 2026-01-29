"""
Yield Risk Monitor.
Analyzes default risk in Private Credit and TVL drops in DeFi.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class YieldRiskMonitor:
    """Monitors yield protocol health."""
    
    def check_defi_health(self, protocol_name: str, current_tvl: float, prev_tvl: float) -> str:
        tvl_drop = (prev_tvl - current_tvl) / prev_tvl if prev_tvl > 0 else 0
        
        if tvl_drop > 0.20:
             logger.critical(f"DEFI_RISK: {protocol_name} TVL dropped {tvl_drop*100:.1f}%. UNSTAKE RECOMMENDED.")
             return "CRITICAL"
        return "HEALTHY"
