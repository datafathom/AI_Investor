import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FlowProcessor:
    """Processes net flows into actionable insights and AUM updates."""
    
    OUTFLOW_ALERT_THRESHOLD = -1000000000.0 # -$1B

    def process_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        ticker = flow_data.get("ticker")
        net_flow = float(flow_data.get("net_flow_usd", 0.0))
        
        # logic to determine if flow is outlier
        is_significant = net_flow < self.OUTFLOW_ALERT_THRESHOLD
        
        return {
            "ticker": ticker,
            "net_flow": net_flow,
            "significant_outflow": is_significant,
            "impact_on_market_cap": net_flow * 1.5 # Multiplier effect
        }
