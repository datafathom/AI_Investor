"""
Logic-Based Justification Logger.
Generates 'Retail-free' justifications for trade entries.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class LogicLogger:
    """
    Translates raw indicator data into institutional logic strings.
    """

    @staticmethod
    def build_justification(
        symbol: str,
        regime: str, # BULLISH, BEARISH, RANGE
        zones: List[Dict],
        order_blocks: List[Dict],
        sentiment: Dict[str, Any]
    ) -> str:
        """
        Construct a logic-based thesis.
        Example: "EUR/USD is currently BULLISH. Entry triggered by Mitigation of Demand Zone at 1.0850. OB Cluster confirmed."
        """
        parts = [f"{symbol} market structure is {regime}."]
        
        if zones:
            active_zones = [z for z in zones if not z.get('mitigated', False)]
            if active_zones:
                parts.append(f"Price is reacting to {active_zones[0]['type']} zone at {active_zones[0]['price_low']}.")

        if order_blocks:
            # Prioritize blocks matching regime
            matching = [ob for ob in order_blocks if (regime == 'BULLISH' and ob['type'] == 'BULLISH_OB') 
                        or (regime == 'BEARISH' and ob['type'] == 'BEARISH_OB')]
            selected = matching[0] if matching else order_blocks[0]
            parts.append(f"Institutional footprints confirmed via {selected['type']}.")

        if sentiment.get('institutional_bias') == 'LONG':
            parts.append("Large Speculator positioning supports upward expansion.")

        return " ".join(parts)

    @staticmethod
    def log_logic(thesis: str):
        """Standard log but with special tag for forensics."""
        logger.info(f"[INSTITUTIONAL_LOGIC] {thesis}")
