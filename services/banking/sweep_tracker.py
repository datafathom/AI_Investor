import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SweepTracker:
    """Tracks bank sweep interest rates vs high-yield alternatives."""
    
    DEFAULT_SWEEP_RATES = {
        "SCHWAB": 0.0045,  # 0.45%
        "FIDELITY": 0.0270, # 2.70%
        "VANGUARD": 0.0470 # 4.70%
    }

    def compare_rates(self, current_custodian: str, hysa_rate: float) -> Dict[str, Any]:
        sweep_rate = self.DEFAULT_SWEEP_RATES.get(current_custodian.upper(), 0.001)
        spread = hysa_rate - sweep_rate
        
        logger.info(f"BANK_LOG: Spread for {current_custodian}: {spread*100:.2f}% vs HYSA {hysa_rate*100:.2f}%")
        
        return {
            "custodian_rate": sweep_rate,
            "alternative_rate": hysa_rate,
            "opportunity_cost_bps": round(spread * 10000, 0),
            "recommendation": "SWEEP_TO_HYSA" if spread > 0.01 else "STAY"
        }
