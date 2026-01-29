
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TrustVsProbateComparison:
    """
    Generates a side-by-side comparison of Trust vs Probate transfers.
    """
    
    def generate_comparison(self, asset_value: float, probate_fees: float, probate_months: int) -> Dict[str, Any]:
        """
        Returns comparison data for the UI.
        """
        comparison = {
            "probate": {
                "transfer_type": "Public / Court Supervised",
                "estimated_cost": probate_fees,
                "estimated_time": f"{probate_months} months",
                "privacy": "Public Record",
                "control": "Court/Executor"
            },
            "trust": {
                "transfer_type": "Private / Autonomous",
                "estimated_cost": 2500.0,  # Estimated post-death admin cost
                "estimated_time": "1-3 months",
                "privacy": "Private Document",
                "control": "Successor Trustee"
            }
        }
        
        savings = probate_fees - 2500.0
        time_saved = probate_months - 2
        
        logger.info(f"Trust vs Probate: Savings=${savings}, TimeSaved={time_saved} months")
        
        return {
            "comparison": comparison,
            "value_propositions": {
                "monetary_savings": savings,
                "time_savings_months": time_saved,
                "privacy_preserved": True
            }
        }
