import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DemographicRiskMonitor:
    """
    Phase 182.5: Ticking Time Bomb 401k Net Outflow Alert.
    Monitors Boomer withdrawals vs Gen Z contributions.
    """
    
    def calculate_net_flow_status(
        self, 
        boomer_withdrawals_b: float, 
        genz_contributions_b: float
    ) -> Dict[str, Any]:
        """
        Alert when Net Flows turn negative due to demographic aging.
        """
        net_flow = genz_contributions_b - boomer_withdrawals_b
        is_bomb_ticking = net_flow < 0
        
        logger.info(f"ALERT_LOG: Net 401k Flow: ${net_flow:.1f}B. Bomb Ticking: {is_bomb_ticking}")
        
        return {
            "boomer_withdrawals": boomer_withdrawals_b,
            "genz_contributions": genz_contributions_b,
            "net_flow_b": round(net_flow, 2),
            "status": "TICKING_TIME_BOMB" if is_bomb_ticking else "SUSTAINABLE",
            "recommendation": "HEDGE_PASSIVE_EXPOSURE" if is_bomb_ticking else "MAINTAIN_INDEXING"
        }
